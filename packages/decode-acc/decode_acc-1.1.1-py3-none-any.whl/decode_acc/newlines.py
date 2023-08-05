"""Separate a stream of text into lines."""

# Copyright (c) 2018, 2020  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


# import abc
import dataclasses
import functools

from typing import List, Optional, Tuple  # noqa: H301


@dataclasses.dataclass(frozen=True)
# class TextSplitter(metaclass=abc.ABCMeta):
class TextSplitter:
    """Base class for building text splitters.

    Test splitters are objects that are fed characters and spit out
    fully-formed lines.
    """

    buf: str = ""
    lines: List[str] = dataclasses.field(default_factory=list)
    done: bool = False

    def add(self, char: Optional[str]) -> "TextSplitter":
        """Process a character or, if None, finalize the splitting as needed.

        Note: this method only handles the None case; derived classes must
        override it to actually process characters and form lines.
        """
        if char is not None:
            raise NotImplementedError(
                "{tname}.add() must be overridden".format(
                    tname=type(self).__name__
                )
            )

        if self.buf:
            return type(self)(buf="", lines=self.lines + [self.buf], done=True)

        return type(self)(buf=self.buf, lines=self.lines, done=True)

    def add_string(self, text: str) -> "TextSplitter":
        """Process all the characters in the specified string."""
        return functools.reduce(lambda spl, char: spl.add(char), text, self)

    def pop_lines(self) -> Tuple["TextSplitter", List[str]]:
        """Extract (into a new object) the accumulated full lines.

        Return a tuple with two elements:
        - an object with the same incomplete line buffer, but
          without the accumulated full lines
        - the full lines accumulated so far
        """
        if not self.lines:
            return (self, [])

        return (type(self)(buf=self.buf, lines=[], done=self.done), self.lines)

    def __str__(self) -> str:
        return "{tname}: {ln} lines + {lbuf} characters, {sdone}done".format(
            tname=type(self).__name__,
            ln=len(self.lines),
            lbuf=len(self.buf),
            sdone="" if self.done else "not ",
        )


@dataclasses.dataclass(frozen=True)
class UniversalNewlines(TextSplitter):
    """Simulate the Python traditional "universal newlines" behavior.

    Split a string into text lines in a manner similar to the file class's
    universal newlines mode: detect LF, CR/LF, and bare CR line terminators.
    """

    preserve: bool = False
    was_cr: bool = False

    def add(self, char: Optional[str]) -> TextSplitter:
        """Add a character to the buffer, and split out a line if needed.

        The line is split out depending on the character being CR or LF and on
        the previous state of the buffer (e.g. detecting CR/LF combinations).
        """

        # pylint: disable=too-many-return-statements

        def newline(eol: str) -> TextSplitter:
            """Turn the accumulated buffer into a new line."""
            line = self.buf + (eol if self.preserve else "")
            return type(self)(
                buf="",
                lines=self.lines + [line],
                done=self.done,
                preserve=self.preserve,
                was_cr=False,
            )

        if char is None:
            if self.was_cr:
                return newline("\r").add(char)
            return super().add(char)

        assert not self.done
        if self.was_cr:
            if char == "\n":
                return newline("\r\n")
            return newline("\r").add(char)

        if char == "\n":
            return newline("\n")
        if char == "\r":
            return type(self)(
                buf=self.buf,
                lines=self.lines,
                done=self.done,
                preserve=self.preserve,
                was_cr=True,
            )

        return type(self)(
            buf=self.buf + char,
            lines=self.lines,
            done=self.done,
            preserve=self.preserve,
            was_cr=self.was_cr,
        )

    def __str__(self) -> str:
        return (
            "UniversalNewlines: {ln} lines + {lbuf} characters, "
            "{sdone} done, {spres}preserve ".format(
                ln=len(self.lines),
                lbuf=len(self.buf),
                sdone="" if self.done else "not ",
                spres="" if self.preserve else "do not ",
            )
        )


@dataclasses.dataclass(frozen=True)
class NullSplitter(TextSplitter):
    """Do not split the text at all."""

    def add(self, char: Optional[str]) -> TextSplitter:
        """Add a character to the buffer without any checks."""
        if char is None:
            return super().add(char)

        assert not self.done
        return type(self)(
            buf=self.buf + char, lines=self.lines, done=self.done
        )

    def __str__(self) -> str:  # pylint: disable=useless-super-delegation
        return super().__str__()


@dataclasses.dataclass(frozen=True)
class FixedEOLSplitter(TextSplitter):
    r"""Split a string into lines using a fixed line separator.

    The separator may consist of more than one character, e.g. '\r\n'.
    """

    eol: str = "\n"
    in_eol: int = 0

    def add(self, char: Optional[str]) -> TextSplitter:
        """Process a new character, possibly part of a line separator."""
        if char is None:
            if self.in_eol > 0:
                return type(self)(
                    buf=self.buf + self.eol[: self.in_eol],
                    lines=self.lines,
                    done=self.done,
                    eol=self.eol,
                    in_eol=0,
                ).add(char)
            return super().add(char)

        assert not self.done
        if char == self.eol[self.in_eol]:
            if self.in_eol + 1 == len(self.eol):
                return type(self)(
                    buf="",
                    lines=self.lines + [self.buf],
                    done=self.done,
                    eol=self.eol,
                    in_eol=0,
                )

            return type(self)(
                buf=self.buf,
                lines=self.lines,
                done=self.done,
                eol=self.eol,
                in_eol=self.in_eol + 1,
            )
        if self.in_eol > 0:
            nspl = type(self)(
                buf=self.buf + self.eol[0],
                lines=self.lines,
                done=self.done,
                eol=self.eol,
                in_eol=0,
            )  # type: TextSplitter
            to_add = self.eol[1 : self.in_eol] + char
            for add_char in to_add:
                nspl = nspl.add(add_char)
            return nspl
        return type(self)(
            buf=self.buf + char,
            lines=self.lines,
            done=self.done,
            eol=self.eol,
            in_eol=self.in_eol,
        )

    def __str__(self) -> str:
        return (
            "{tname}: {ln} lines + {lbuf} characters, {sdone}done, "
            "eol {eol}".format(
                tname=type(self).__name__,
                ln=len(self.lines),
                lbuf=len(self.buf),
                sdone="" if self.done else "not ",
                eol=repr(self.eol),
            )
        )


def get_dwim_splitter(newline: Optional[str] = None) -> TextSplitter:
    """Choose a splitter class in a manner similar to open().

    If None is passed for the newline parameter, universal newlines mode
    will be enabled and the line terminators will not be present in
    the returned lines.  If newline is an empty string, universal newlines
    mode is enabled, but the line terminators will be preserved.
    If newline has any other value, it is used as a line terminator and
    stripped from the returned lines.
    """
    if newline is None:
        return UniversalNewlines()
    if newline == "":
        return UniversalNewlines(preserve=True)
    return FixedEOLSplitter(eol=newline)
