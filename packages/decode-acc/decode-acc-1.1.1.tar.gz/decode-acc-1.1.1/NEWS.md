# Change log for decode-acc, the incremental decoder

1.1.1
-----

* Miscellaneous changes:

  - describe the `decode_acc.util` functions and classes in the README file

  - fix a typographical error in a docstring

1.1.0
-----

- Functionality changes:

  * reraise a `UnicodeDecodeError` if there is no possible way any more
    added bytes would allow the previous ones to form a valid character

  * use dataclasses instead of hand-rolled value objects

  * add the `decode_acc.util` module containing the `detect_utf8_locale()`
    and `get_utf8_env()` functions and the `Config` and `ConfigProc` classes

- Test suite changes:

  * use pytest instead of os-testr

  * add a testing environment using the OpenStack `hacking` module

  * drop the `skipsdist` option, let `tox` roll up a dist archive

  * various minor `tox.ini` improvements

- Miscellaneous changes:

  * reformat the source code using the `black` tool

  * list Python 3.8 as a supported version

  * push the source files down into a `src/` subdirectory

1.0.0
-----

- First public release.
