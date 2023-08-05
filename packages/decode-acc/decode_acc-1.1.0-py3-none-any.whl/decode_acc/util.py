"""Utility functions loosely related to UTF-8 processing."""

import dataclasses
import os
import pathlib
import subprocess
import sys

from typing import (
    Dict,  # noqa: H301
    IO,
    List,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Union,
)


UTF8_LANGUAGES = ("C", "en_US", "en", "en_UK", "en_CA", "en_AU")
UTF8_ENCODINGS = ("UTF-8", "utf8")


if TYPE_CHECKING:
    Path = os.PathLike[str]  # pylint: disable=unsubscriptable-object
    Popen = subprocess.Popen[str]  # pylint: disable=unsubscriptable-object
else:
    Path = os.PathLike
    Popen = subprocess.Popen

PathSeq = Sequence[Union[Path, str]]
PathList = List[Union[Path, str]]


def detect_utf8_locale() -> str:
    """Get a locale name that may hopefully be used for UTF-8 output."""
    all_locales = set(
        subprocess.check_output(
            ["env", "LC_ALL=C", "LANGUAGE=", "locale", "-a"],
            shell=False,
            encoding="ISO-8859-1",
        ).splitlines()
    )

    for lang in UTF8_LANGUAGES:
        for enc in UTF8_ENCODINGS:
            name = f"{lang}.{enc}"
            if name in all_locales:
                return name

    return "C"


def get_utf8_env(env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Prepare the environment to run subprocesses in.

    This function uses `detect_utf8_locale()` and then returns a new
    dictionary modified to set the `LC_ALL` variable to the name of
    the obtained locale and to unset the `LANGUAGE` variable to avoid
    applications that use the `gettext` library still using another
    language/locale setting.
    """
    utf8loc = detect_utf8_locale()
    subenv = dict(os.environ if env is None else env)
    subenv["LC_ALL"] = utf8loc
    subenv["LANGUAGE"] = ""
    return subenv


@dataclasses.dataclass(frozen=True)
class Config:
    """Basic runtime configuration class.

    This class defines a 'verbose' flag and a `diag()` method that
    outputs a message to the standard error stream if the `verbose`
    flag is set to a true value.
    """

    verbose: bool

    def diag(self, msg: str) -> None:
        """Output a diagnostic message if requested."""
        if self.verbose:
            print(msg, file=sys.stderr)


@dataclasses.dataclass(frozen=True)
class ConfigProc(Config):
    """A configuration class providing subprocess helpers."""

    sub_locale: str = dataclasses.field(init=False)
    sub_env: Dict[str, str] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """Set up the locale and environment to use for child processes."""
        object.__setattr__(self, "sub_env", get_utf8_env())
        object.__setattr__(self, "sub_locale", self.sub_env["LC_ALL"])

    def check_call(
        self,
        cmd: PathSeq,
        *,
        shell: bool = False,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[pathlib.Path] = None,
    ) -> None:
        """Run a child process in a UTF-8 locale."""
        subprocess.check_call(
            cmd,
            shell=shell,
            env=env if env is not None else self.sub_env,
            cwd=cwd,
        )

    def check_output(
        self,
        cmd: PathSeq,
        *,
        shell: bool = False,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[pathlib.Path] = None,
        encoding: str = "UTF-8",
        bufsize: int = 0,
    ) -> str:
        """Run a child process in a UTF-8 locale."""
        # pylint: disable=unexpected-keyword-arg
        # https://github.com/PyCQA/astroid/pull/795
        return subprocess.check_output(
            cmd,
            shell=shell,
            env=env if env is not None else self.sub_env,
            cwd=cwd,
            encoding=encoding,
            bufsize=bufsize,
        )

    def Popen(  # pylint: disable=invalid-name
        self,
        cmd: PathSeq,
        *,
        shell: bool = False,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[pathlib.Path] = None,
        encoding: str = "UTF-8",
        bufsize: int = 0,
        stdin: Optional[Union[int, IO[str]]] = None,
        stdout: Optional[Union[int, IO[str]]] = None,
        stderr: Optional[Union[int, IO[str]]] = None,
    ) -> Popen:
        """Run a child process in a UTF-8 locale."""
        # pylint: disable=unexpected-keyword-arg
        # https://github.com/PyCQA/astroid/pull/795
        return subprocess.Popen(
            cmd,
            shell=shell,
            env=env if env is not None else self.sub_env,
            cwd=cwd,
            encoding=encoding,
            bufsize=bufsize,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
        )
