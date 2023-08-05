"""Some basic tests for the DecodeAccumulator class."""

# Copyright (c) 2018 - 2020  Peter Pentchev <roam@ringlet.net>
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


import unittest

from typing import Dict, List  # noqa: H301

import ddt  # type: ignore
import pytest

import decode_acc

from decode_acc import newlines

from . import data as test_data


@ddt.ddt
class TestInitialization(unittest.TestCase):
    """Test basic class initialization."""

    # pylint: disable=no-self-use

    @ddt.data(*test_data.ENCODINGS)
    def test_str_repr(self, encoding: str) -> None:
        """Test some basic aspects of a newly-initialized accumulator."""
        acc = decode_acc.accumulator.DecodeAccumulator(encoding=encoding)
        assert acc.encoding == encoding
        assert not acc.buf
        assert not acc.decoded

        str_desc = str(acc)
        assert str_desc.startswith("DecodeAccumulator: ")
        assert ' encoding "{enc}"'.format(enc=encoding) in str_desc
        assert " 0 raw bytes" in str_desc
        assert " 0 decoded characters" in str_desc
        assert " not done" in str_desc

        str_repr = repr(acc)
        assert str_repr.startswith("DecodeAccumulator(")
        assert "encoding='{enc}'".format(enc=encoding) in str_repr
        assert "decoded=''" in str_repr
        assert "done=False" in str_repr


@ddt.ddt
class TestDecode(unittest.TestCase):
    """Test incremental decoding."""

    # pylint: disable=no-self-use

    @ddt.data(*test_data.TEST_DATA_LIST)
    @ddt.unpack
    def test_decode(
        self, tdata: List[int], enc_name: str, enc_data: Dict[str, List[int]]
    ) -> None:
        """Actually test the incremental decoding of characters.

        Actually test the accumulator's capabilities of incrementally
        decoding characters in the specified encoding, along with its
        internal state at each step.
        """
        data = bytes(tdata)
        acc = decode_acc.accumulator.DecodeAccumulator(encoding=enc_name)
        multiplier = 1
        for i in range(len(data)):
            old_repr = repr(acc)
            try:
                nacc = acc.add(data[i : i + 1])
            except UnicodeDecodeError:
                multiplier = -1
            assert repr(acc) == old_repr
            acc = nacc
            assert len(acc.decoded) == multiplier * enc_data["length"][i]
            assert len(acc.buf) == enc_data["length-raw"][i]
            assert not acc.done

        old_repr = repr(acc)
        (nacc, text) = acc.pop_decoded()
        assert repr(acc) == old_repr
        assert nacc.encoding == acc.encoding
        assert nacc.buf == acc.buf
        assert nacc.decoded == ""
        assert not nacc.done
        assert len(text) == multiplier * enc_data["length"][-1]

        old_repr = repr(acc)
        nacc = acc.add(None)
        assert repr(acc) == old_repr
        assert nacc.encoding == acc.encoding
        assert nacc.buf == acc.buf
        assert nacc.decoded == acc.decoded
        assert nacc.done
        with pytest.raises(AssertionError):
            nacc.add("a".encode("us-ascii"))


@ddt.ddt
class TestSplit(unittest.TestCase):
    """Test a decoder-splitter combination."""

    # pylint: disable=no-self-use

    @ddt.data(*test_data.TEST_DATA_LIST)
    @ddt.unpack
    def test_split(
        self, tdata: List[int], enc_name: str, enc_data: Dict[str, List[int]]
    ) -> None:
        """Test incremental splitting during the incremental decoding."""
        data = bytes(tdata)
        acc = decode_acc.accumulator.DecodeAccumulator(encoding=enc_name)
        spl = newlines.UniversalNewlines()  # type: newlines.TextSplitter
        multiplier = 1
        for i in range(len(data)):
            try:
                (acc, decoded) = acc.add(data[i : i + 1]).pop_decoded()
            except UnicodeDecodeError:
                multiplier = -1
            spl = spl.add_string(decoded)
            assert len(spl.buf) == multiplier * enc_data["length-lines"][i]
            assert len(spl.lines) == multiplier * enc_data["lines"][i]
            assert not spl.done
