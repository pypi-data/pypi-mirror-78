# An incremental decoder of bytes into characters and lines

## The DecodeAccumulator class

The `DecodeAccumulator` class implements an incremental decoder: an object
that may be fed bytes (one or several at a time) as they are e.g. read
from a network stream or a subprocess's output, and that adds to a result
string as soon as enough bytes have been accumulated to produce a character
in the specified encoding.

Note that `DecodeAccumulator` objects are immutable value objects:
the `add()` method does not modify its invocant, but returns a new
`DecodeAccumulator` object instead.

Sample usage:

    while True:
        bb = subprocess.stdout.read(1024)
        if len(bb) == 0:
            break
        acc = acc.add(bb)
        assert(not acc.done)
        if acc.splitter.lines:
            # at least one full line was produced
            (acc, lines) = acc.pop_lines()
            print('\n'.join(lines)

    if acc.buf:
        print('Leftover bytes left in the buffer!', file=sys.stderr)

    if acc.splitter.buf:
        print('Incomplete line: ' + acc.splitter.buf)

    final = acc.add(None)
    assert(final.splitter.buf == '')
    assert(final.splitter.done)
    assert(final.done)
    if acc.splitter.buf:
        assert(len(final.splitter.lines) == len(acc.splitter.lines) + 1)

## The splitter classes: UniversalNewlines, FixedEOLSplitter, NullSplitter

The `decode_acc.newlines` module provides three classes that may be used to
split a text string into lines in different ways.  The `UniversalNewlines`
class does its best to simulate the "universal newlines" behavior of `file`
objects.  The `FixedEOLSplitter` class uses a specified string as a line
terminator to split on.  The `NullSplitter` class does not do any splitting.

Sample usage:

    spl = newlines.UniversalNewlines()
    for char in input_string:
        spl = spl.add(char)
    spl.add(None)

    for (idx, line) in enumerate(spl.lines):
        print('line {idx}: {line}'.format(idx=idx, line=line))

## The UTF-8 environment setup functions: detect\_utf8\_locale(), get\_utf8\_env()

The `decode_acc.util` module provides two functions that are useful for
setting up an environment in which to run child processes.

The `detect_utf8_locale()` function runs the external `locale` command to
obtain a list of the supported locale names, and then picks a suitable one to
use so that programs are more likely to output valid UTF-8 characters and
language-neutral messages. It prefers the `C` base locale, but if neither
`C.UTF-8` nor `C.utf8` is available, it will fall back to a list of other
locale names that are likely to be present on the system.

The `get_utf8_env()` function invokes `detect_utf8_locale()` and then returns
a dictionary similar to `os.environ`, but with `LC_ALL` set to the obtained
locale name and `LANGUAGE` set to an empty string so that recent versions of
the gettext library do not choose a different language to output messages in.
If a dictionary is passed as the `env` parameter, `get_utf8_env()` uses it as
a base instead of the value of `os.environ`.

## The configuration classes: Config, ConfigProc

The `decode_acc.util` module also provides two dataclasses that may be used as
base classes for program configuration data, usually runtime settings
obtained from command-line options. Their main purpose, however, or rather
the main purpose of the `ConfigProc` class, is to provide automated
detection of the UTF-8 locale to use and supply helper methods similar to
the functions and classes provided by the `subprocess` module for
starting child processes in an UTF-8 environment.

The `Config` class has a single field, the `verbose` boolean flag.
It also provides the `diag()` method that will check the `verbose` flag and
output the specified message to the standard error stream (in order not to
intersperse program output and diagnostic messages on the standard output
stream) if requested.

The `ConfigProc` class extends the `Config` class with three methods,
`check_call()`, `check_output()`, and `Popen()`, that accept exactly
the same arguments as the corresponding symbols from the `subprocess` module,
but provide default values for some of them. In particular:

- `env` uses the environment returned by `get_utf8_env()`

- `encoding` uses the string returned by `detect_utf8_locale()`

- `shell` is set to `False` unless specified

Sample usage:

    import dataclasses

    from decode_acc import util as d_util

    @dataclasses.dataclass(frozen=True)
    class Config(d_util.ConfigProc):
        """Runtime configuration for the hello program."""

        target: str


    ...
    cfg = Config(target="world", verbose=True)
    ...
    cfg.diag(f"About to greet {cfg.target}")
    cfg.check_call(["printf", "--", "Hello, %s!\\n", cfg.target])


## License and copyright

    Copyright (c) 2018 - 2020  Peter Pentchev <roam@ringlet.net>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
    OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
