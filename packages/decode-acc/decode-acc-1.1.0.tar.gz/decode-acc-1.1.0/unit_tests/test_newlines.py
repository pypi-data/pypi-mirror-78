"""Test the text splitters in the newlines submodule."""

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


import itertools
import unittest

from typing import List, Tuple, Union  # noqa: H301

import ddt  # type: ignore

from decode_acc import newlines

from . import data as test_data


def process_data(
    splitter: newlines.TextSplitter, skip: int = 0, as_string: bool = False
) -> newlines.TextSplitter:
    """Run the test data through the specified splitter."""
    data = test_data.TEST_SPLIT.data[skip:]
    data_str = "".join([chr(char) for char in data])
    if as_string:
        splitter = splitter.add_string(data_str)
    else:
        for char in data_str:
            splitter = splitter.add(char)
    return splitter.add(None)


@ddt.ddt
class TestSplit(unittest.TestCase):
    """Test the various ways of splitting text into lines."""

    # pylint: disable=no-self-use

    @ddt.data(False, True)
    def test_non_split(self, as_string: bool) -> None:
        """Test not splitting text into lines at all."""
        splitter = process_data(newlines.NullSplitter(), as_string=as_string)
        assert splitter.buf == ""
        assert len(splitter.lines) == 1
        assert len(splitter.lines[0]) == len(test_data.TEST_SPLIT.data)
        assert splitter.done

    @ddt.data(False, True)
    def test_universal(self, as_string: bool) -> None:
        """Test the universal newlines splitter."""
        splitter = process_data(newlines.UniversalNewlines())
        assert [
            len(line) for line in splitter.lines
        ] == test_data.TEST_SPLIT.eol["none"]

        splitter = process_data(
            newlines.UniversalNewlines(preserve=True), as_string=as_string
        )
        assert [
            len(line) for line in splitter.lines
        ] == test_data.TEST_SPLIT.eol[""]

    @ddt.data(*itertools.product(("\r", "\n", "\r\n"), (False, True)))
    @ddt.unpack
    def test_fixed(self, eol: str, as_string: bool) -> None:
        """Test the fixed line terminator splitter."""
        splitter = process_data(
            newlines.FixedEOLSplitter(eol=eol), as_string=as_string
        )
        assert [
            len(line) for line in splitter.lines
        ] == test_data.TEST_SPLIT.eol[eol]


SplitterElemType = Tuple[int, newlines.TextSplitter]


class TestRelations(unittest.TestCase):
    """Test relations between various ValueObjects."""

    def setUp(self) -> None:
        """Create a series of splitters."""
        self.splitters = [[], []]  # type: List[List[SplitterElemType]]
        for skip in range(2):
            for _ in range(4):
                self.splitters[skip].append(
                    (1, process_data(newlines.NullSplitter(), skip=skip))
                )
                self.splitters[skip].append(
                    (2, process_data(newlines.UniversalNewlines(), skip=skip))
                )
                self.splitters[skip].append(
                    (
                        3,
                        process_data(
                            newlines.UniversalNewlines(preserve=True),
                            skip=skip,
                        ),
                    )
                )
                self.splitters[skip].append(
                    (
                        4,
                        process_data(
                            newlines.FixedEOLSplitter(eol="\r"), skip=skip
                        ),
                    )
                )
                self.splitters[skip].append(
                    (
                        5,
                        process_data(
                            newlines.FixedEOLSplitter(eol="\n"), skip=skip
                        ),
                    )
                )
                self.splitters[skip].append(
                    (
                        6,
                        process_data(
                            newlines.FixedEOLSplitter(eol="\r\n"), skip=skip
                        ),
                    )
                )

    def test_eq(self) -> None:
        """Test splitters for equality."""
        # First test that splitters within each set are pretty much equal
        for skip in range(2):
            combos = itertools.combinations(self.splitters[skip], 2)
            for ((tag_first, first), (tag_second, second)) in combos:
                if tag_first == tag_second:
                    assert first == second
                else:
                    assert first != second

        # Now make sure that the splitters differ between sets
        combos = itertools.product(self.splitters[0], self.splitters[1])
        for ((tag_first, first), (tag_second, second)) in combos:
            assert first != second


@ddt.ddt
class TestDWIM(unittest.TestCase):
    """Test the do-what-I-mean helper function."""

    # pylint: disable=no-self-use

    @ddt.data(
        *itertools.product(test_data.TEST_SPLIT.eol.items(), (False, True))
    )
    @ddt.unpack
    def test_split(
        self, eol_data: Tuple[Union[str, None], List[int]], as_string: bool
    ) -> None:
        """Test various splitting techniques."""
        (eol, lines) = eol_data
        if eol == "none":
            eol = None
        splitter = newlines.get_dwim_splitter(eol)
        assert splitter.lines == []
        assert not splitter.done

        splitter = process_data(splitter, as_string=as_string)
        assert [len(line) for line in splitter.lines] == lines
        assert splitter.done
