"""Packaging metadata for the decode-acc library."""

# Copyright (c) 2018 - 2020  Peter Pentchev
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

import pathlib
import re
import setuptools  # type: ignore


RE_VERSION = re.compile(
    r"""^
    \s* VERSION \s* = \s* "
    (?P<version>
           (?: 0 | [1-9][0-9]* )    # major
        \. (?: 0 | [1-9][0-9]* )    # minor
        \. (?: 0 | [1-9][0-9]* )    # patchlevel
    (?: \. [a-zA-Z0-9]+ )?          # optional addendum (dev1, beta3, etc.)
    )
    " \s*
    $""",
    re.X,
)


def get_version() -> str:
    """Get the module version from its __init__.py file."""
    found = [
        data.group("version")
        for data in (
            RE_VERSION.match(line)
            for line in pathlib.Path("src/decode_acc/__init__.py").open(
                encoding="UTF-8"
            )
        )
        if data
    ]
    assert len(found) == 1
    return found[0]


def get_long_description() -> str:
    """Read the long description from the README.md file."""
    return pathlib.Path("README.md").read_text(encoding="UTF-8")


setuptools.setup(
    name="decode-acc",
    version=get_version(),
    description="Incrementally decode bytes into strings and lines",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Peter Pentchev",
    author_email="roam@ringlet.net",
    url="https://gitlab.com/ppentchev/decode-acc/",
    packages=("decode_acc",),
    package_dir={"": "src"},
    package_data={
        "decode_acc": [
            # The PEP 484 typed Python module marker
            "py.typed"
        ]
    },
    license="BSD-2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: DFSG approved",
        "License :: Freely Distributable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">= 3.6",
    install_requires=["dataclasses; python_version < '3.7'"],
    tests_require=["dataclasses; python_version < '3.7'", "ddt", "pytest"],
    zip_safe=True,
)
