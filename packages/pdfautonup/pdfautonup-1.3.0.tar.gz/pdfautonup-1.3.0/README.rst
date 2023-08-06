pdfautonup 🍳 n-up the pages of pdf files, guessing layout
==========================================================

Fit as much pages as possible, from some PDF files to a 'n-up' PDF file of a given page size, guessing the layout.

Examples
--------

With the default paper size being A4, ``pdfautonup`` on:

- `trigo.pdf <https://framagit.org/spalax/pdfautonup/-/raw/master/examples/trigo.pdf?inline=false>`_ gives `trigo-nup.pdf <https://framagit.org/spalax/pdfautonup/-/raw/master/examples/trigo-nup.pdf?inline=false>`_
- `pcb.pdf <https://framagit.org/spalax/pdfautonup/-/raw/master/examples/pcb.pdf?inline=false>`_ gives `pcb-nup.pdf <https://framagit.org/spalax/pdfautonup/-/raw/master/examples/pcb-nup.pdf?inline=false>`_
- `three-pages.pdf <https://framagit.org/spalax/pdfautonup/-/raw/master/examples/three-pages.pdf?inline=false>`_ gives `three-pages-nup.pdf <https://framagit.org/spalax/pdfautonup/-/raw/master/examples/three-pages-nup.pdf?inline=false>`_

See the documentation for the full command lines used to generate those examples.

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/pdfautonup/blob/master/CHANGELOG.md>`_.

Download and install
--------------------

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/pdfautonup
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 setup.py install

* From pip::

    pip install pdfautonup

  Note: If `PyMuPDF <https://github.com/pymupdf/PyMuPDF>`_ can be installed, you can use::

    pip install pdfautonup[pymupdf]

  This will change the python library used to read and write PDF files (`PyMuPDF <https://github.com/pymupdf/PyMuPDF>`_ instead of `PyPDF2 <http://mstamy2.github.io/PyPDF2/>`_), to make pdfautonup faster.

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ (and `setuptools-scm <https://pypi.org/project/setuptools-scm/>`_) to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/pdfautonup-<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://pdfautonup.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html
