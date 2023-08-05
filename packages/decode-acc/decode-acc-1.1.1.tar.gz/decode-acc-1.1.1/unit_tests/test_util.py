"""Test the UTF-8-related decode_acc.util functions."""

import dataclasses
import os
import subprocess

from typing import Dict

from decode_acc import util


LANG_KEYS = set(["LC_ALL", "LANGUAGE"])


def check_env(env: Dict[str, str]) -> None:
    """Make sure a UTF8-capable environment was setup correctly."""
    # Everything except LANG_KEYS is the same as in os.environ
    assert {
        key: value for key, value in env.items() if key not in LANG_KEYS
    } == {
        key: value for key, value in os.environ.items() if key not in LANG_KEYS
    }

    # The rest of this function makes sure that locale(1) and date(1), when
    # run in this environment, output reasonable values
    loc = {
        fields[0]: fields[1].strip('"')
        for fields in (
            line.split("=", 1)
            for line in subprocess.check_output(
                ["locale"], shell=False, env=env, encoding="UTF-8"
            ).splitlines()
        )
    }
    non_lc = set(name for name in loc if not name.startswith("LC_"))
    assert non_lc.issubset(set(("LANG", "LANGUAGE")))
    loc = {
        name: value for name, value in loc.items() if name.startswith("LC_")
    }
    values = list(set(loc.values()))
    assert len(values) == 1, values
    assert values[0].lower().endswith(".utf8") or values[0].lower().endswith(
        ".utf-8"
    )

    utc_env = dict(env)
    utc_env["TZ"] = "UTC"
    lines = subprocess.check_output(
        ["date", "-d", "@1000000000", "+%a %A %b %B"],
        shell=False,
        env=utc_env,
        encoding="UTF-8",
    ).splitlines()
    assert lines == ["Sun Sunday Sep September"]


def test_utf8_env() -> None:
    """Test get_utf8_env() and, indirectly, detect_utf8_locale()."""
    env = util.get_utf8_env()
    check_env(env)

    mod_env = {
        key: value
        for key, value in os.environ.items()
        if key not in ("HOME", "USER", "PS1", "PATH")
    }
    mod_env["TEST_KEY"] = "test value"

    env2 = util.get_utf8_env(mod_env)
    # Nothing besides LANG_KEYS has changed
    assert {
        key: value for key, value in env2.items() if key not in LANG_KEYS
    } == {key: value for key, value in mod_env.items() if key not in LANG_KEYS}

    # LANG_KEYS have changed in the same way as before
    assert {key: value for key, value in env2.items() if key in LANG_KEYS} == {
        key: value for key, value in env.items() if key in LANG_KEYS
    }


def test_config() -> None:
    """Test the Config and ConfigProc classes."""
    cfg = util.Config(verbose=False)
    assert sorted(
        (field.name, field.type) for field in dataclasses.fields(cfg)
    ) == [("verbose", bool)]
    assert not cfg.verbose

    pcfg = util.ConfigProc(verbose=True)
    assert sorted(
        (field.name, field.type) for field in dataclasses.fields(pcfg)
    ) == [("sub_env", Dict[str, str]), ("sub_locale", str), ("verbose", bool)]
    assert pcfg.verbose

    check_env(pcfg.sub_env)

    lines = pcfg.check_output(["printenv", "LC_ALL"]).splitlines()
    assert lines == [pcfg.sub_locale]
    assert lines[0].lower().split(".")[-1] in ("utf8", "utf-8")

    mod_env = dict(pcfg.sub_env)
    mod_env["LC_ALL"] = "nowhere"
    lines = pcfg.check_output(["printenv", "LC_ALL"], env=mod_env).splitlines()
    assert lines == ["nowhere"]
