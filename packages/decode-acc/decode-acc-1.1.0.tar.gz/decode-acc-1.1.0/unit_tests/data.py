"""Test data for the accumulator and splitter tests."""

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


import collections
import itertools


TestData = collections.namedtuple("TestData", ["data", "enc"])

TEST_DATA = [
    TestData(
        data=[65, 33],
        enc={
            "us-ascii": {
                "length": [1, 2],
                "length-raw": [0, 0],
                "length-lines": [1, 2],
                "lines": [0, 0],
            },
            "Latin-1": {
                "length": [1, 2],
                "length-raw": [0, 0],
                "length-lines": [1, 2],
                "lines": [0, 0],
            },
            "windows-1251": {
                "length": [1, 2],
                "length-raw": [0, 0],
                "length-lines": [1, 2],
                "lines": [0, 0],
            },
            "UTF-8": {
                "length": [1, 2],
                "length-raw": [0, 0],
                "length-lines": [1, 2],
                "lines": [0, 0],
            },
        },
    ),
    TestData(
        data=[0x2D, 0xD0, 0xB0, 0x20, 0xD0, 0xB1, 0x21, 0x0A],
        enc={
            "us-ascii": {
                "length": [1, 1, -1, -1, -1, -1, -1, -1],
                "length-raw": [0, 1, 1, 1, 1, 1, 1, 1],
                "length-lines": [1, 1, -1, -1, -1, -1, -1, -1],
                "lines": [0, 0, 0, 0, 0, 0, 0, 0],
            },
            "Latin-1": {
                "length": [1, 2, 3, 4, 5, 6, 7, 8],
                "length-raw": [0, 0, 0, 0, 0, 0, 0, 0],
                "length-lines": [1, 2, 3, 4, 5, 6, 7, 0],
                "lines": [0, 0, 0, 0, 0, 0, 0, 1],
            },
            "windows-1251": {
                "length": [1, 2, 3, 4, 5, 6, 7, 8],
                "length-raw": [0, 0, 0, 0, 0, 0, 0, 0],
                "length-lines": [1, 2, 3, 4, 5, 6, 7, 0],
                "lines": [0, 0, 0, 0, 0, 0, 0, 1],
            },
            "UTF-8": {
                "length": [1, 1, 2, 3, 3, 4, 5, 6],
                "length-raw": [0, 1, 0, 0, 1, 0, 0, 0],
                "length-lines": [1, 1, 2, 3, 3, 4, 5, 0],
                "lines": [0, 0, 0, 0, 0, 0, 0, 1],
            },
        },
    ),
]

TEST_DATA_LIST = list(
    itertools.chain(
        *[[(v.data, i[0], i[1]) for i in v.enc.items()] for v in TEST_DATA]
    )
)

ENCODINGS = sorted(set(itertools.chain(*[v.enc.keys() for v in TEST_DATA])))


TestSplit = collections.namedtuple("TestSplit", ["data", "eol"])


TEST_SPLIT = TestSplit(
    data=[0x65, 0x0A, 0x33, 0x0D, 0x0D, 0x0A, 0x21, 0x0D, 0x22, 0x0A, 0x0D],
    eol={
        "none": [1, 1, 0, 1, 1, 0],
        "": [2, 2, 2, 2, 2, 1],
        "\n": [1, 3, 3, 1],
        "\r": [3, 0, 2, 2],
        "\r\n": [4, 5],
    },
)
