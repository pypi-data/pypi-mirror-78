* pdfautonup 1.3.0 (2020-09-07)

    * Python support:
      * Drop python3.5 support.
      * Add python3.9 support.
    * Fix bug: PyPDF2 backend would crash with a valid pdf file without any trailing info (thanks Alex Dong).
    * Fix typo in documentation.

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 1.2.0 (2019-09-07)

    * Python support
      * Drop python3.6 support.
      * Add python3.8 support
    * It is now possible to choose the Python library used to read and write
      PDF files (closes #14).

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 1.1.0 (2019-03-08)

    * Python support
      * Drop python3.4 support.
      * Python3.7 support
    * Dependencies
      * Replace PyPDF2 dependency with PyMuPDF.
    * Features and Bugs
      * Pdfautonup is faster (closes #9).
      * Can read and write from standard input and input (closes #12).
      * Pages are cropped before being merged (closes #13).

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 1.0.0 (2017-12-06)

    * Log a warning if pages have different sizes.

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.4.3 (2017-03-11)

    * No longer crash if PDF files have no pages (closes #10).
    * No longer crash if PDF pages have null dimensions, for instance "0cmx1cm" (closes #11).
    * Add python3.6 support.
    * Add regression tests.
    * Minor internal improvements.

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.4.2 (2016-10-14)

    * Move help about paper sizes into a separate "--help-paper" option.

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.4.1 (2016-05-21)

    * Fix error in changelog.

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.4.0 (2016-05-21)

    * Raise error instead of producing a PDF with no pages (closes #7).
    * Add option `--progress` (closes #8).

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.3.0 (2016-02-18)

    * New algorithm to arrange source documents onto destination document (from a request to panelize printed circuit boards).
    * Adding other algorithms will be easier now.
    * Add option `--orientation`, to force destination page orientation.
    * Fix centering and margin problems with the `fuzzy` (old) algorithm.
    * Minor documentation improvements

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.2.0 (2016-01-25)

    * Can be called as a python module : `python3 -m pdfautonup FOO` is equivalent to `pdfautonup FOO`.
    * Fix error when `paperconf` is not installed (closes #3).
    * Add `.pdf` to argument if missing (closes #4).

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.1.1 (2015-06-13)

    * Python3.5 support
    * In case of unreadable file (corrupted PDF, not a PDF, no-existant, etc.),
      die nicely (instead of displaying the exception stack).
    * Added project URL to generated pdf metadata
    * Several minor improvements to setup, test and documentation.

    -- Louis Paternault <spalax@gresille.org>

* pdfautonup 0.1.0 (2015-03-20)

    * First published version.

    -- Louis Paternault <spalax@gresille.org>
