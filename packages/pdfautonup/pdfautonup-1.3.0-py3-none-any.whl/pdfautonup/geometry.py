# Copyright Louis Paternault 2014-2019
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Different algorithm to fit source files into destination files."""

from collections import namedtuple
import decimal
import operator
import os

import papersize

from pdfautonup import LOGGER
from pdfautonup import errors
from pdfautonup.pdfbackend.auto import (  # pylint: disable=no-name-in-module
    PDFFileWriter,
)


def _dist_to_round(x):
    """Return distance of ``x`` to ``round(x)``."""
    return abs(x - round(x))


class _Layout:
    def __init__(self, target_size, arguments):
        self.target_size = target_size
        self.interactive = arguments.interactive

        self.pdf = PDFFileWriter()
        self.current_pagenum = 0
        self.current_page = None

    def add_page(self, page):
        """Add ``page`` to the destination file.

        It is added at the right place, and a new blank page is created if
        necessary.
        """
        if self.current_pagenum == 0:
            self.current_page = self.pdf.new_page(
                width=round(self.target_size[0]), height=round(self.target_size[1])
            )
        (x, y) = self.cell_topleft(self.current_pagenum)
        self.current_page.merge_translated_page(page, x, y)
        self.current_pagenum = (self.current_pagenum + 1) % self.pages_per_page

    def write(self, outputname, inputname, *, metadata):
        """Write destination file."""
        # I wonder whether this functions should be woved in another module, or
        # not: it is the only function dealing with file system in this module.
        self._set_metadata(metadata)

        if outputname is None and inputname == "-":
            outputname = "-"
        elif outputname is None:
            outputname = "{}-nup.pdf".format(inputname[: -len(".pdf")])

        if outputname != "-" and self.interactive and os.path.exists(outputname):
            question = "File {} already exists. Overwrite (y/[n])? ".format(outputname)
            if input(question).lower() != "y":
                raise errors.PdfautonupError("Cancelled by user.")

        if outputname == "-":
            self.pdf.write()
        else:
            self.pdf.write(outputname)

    def _set_metadata(self, metadata):
        """Set metadata on current pdf."""
        metadata[
            "producer"
        ] = "pdfautonup, using the PyPDF2 library — http://framagit.org/spalax/pdfautonup"
        self.pdf.metadata = metadata

    def cell_topleft(self, num):
        """Return the top left coordinate of ``num``th cell of page."""
        raise NotImplementedError()

    @property
    def pages_per_page(self):
        """Return the number of source pages per destination page."""
        raise NotImplementedError()


class Fuzzy(_Layout):
    """Documents can overlap, and space can be wasted, but not too much."""

    #: A target size, associated with the number of source pages that will fit
    #: in it, per width and height (``cell_number[0]`` and ``cell_number[1]``).
    Grid = namedtuple("Grid", ["cell_number", "target_size", "margins", "gaps"])

    def __init__(self, source_size, target_size, arguments):
        if arguments.margin[0] is not None or arguments.gap[0] is not None:
            LOGGER.warning(
                "Arguments `--margin` and `--gap` are ignored with algorithm `fuzzy`."
            )
        self.source_size = source_size
        if arguments.orientation == "landscape":
            self.grid = self._grid(
                source_size, papersize.rotate(target_size, papersize.LANDSCAPE)
            )
        elif arguments.orientation == "portrait":
            self.grid = self._grid(
                source_size, papersize.rotate(target_size, papersize.PORTRAIT)
            )
        else:
            self.grid = min(
                self._grid(source_size, target_size),
                self._grid(source_size, (target_size[1], target_size[0])),
                key=self.ugliness,
            )

        super().__init__(self.grid.target_size, arguments)

    def ugliness(self, grid):
        """Return the "ugliness" of this ``grid``.

        - A layout that fits perfectly has an ugliness of 0.
        - The maximum ugliness is 1.
        """
        target_width, target_height = grid.target_size
        source_width, source_height = self.source_size
        return (
            _dist_to_round(target_width / source_width) ** 2
            + _dist_to_round(target_height / source_height) ** 2
        )

    @staticmethod
    def _margins(target_size, source_size, cell_number):
        if cell_number[0] == 1:
            width = (target_size[0] - source_size[0] * cell_number[0]) / 2
        else:
            width = 0
        if cell_number[1] == 1:
            height = (target_size[1] - source_size[1] * cell_number[1]) / 2
        else:
            height = 0
        return [width, height]

    @staticmethod
    def _gaps(target_size, source_size, cell_number):
        if cell_number[0] == 1:
            width = decimal.Decimal(0)
        else:
            width = (target_size[0] - cell_number[0] * source_size[0]) / (
                cell_number[0] - 1
            )
        if cell_number[1] == 1:
            height = decimal.Decimal(0)
        else:
            height = (target_size[1] - cell_number[1] * source_size[1]) / (
                cell_number[1] - 1
            )
        return (width, height)

    def _grid(self, source_size, target_size):
        """Return a :class:`self.Grid` object for arguments.

        The main function is computing the number of source pages per
        destination pages.
        """
        try:
            cell_number = (
                max(1, round(target_size[0] / source_size[0])),
                max(1, round(target_size[1] / source_size[1])),
            )
        except decimal.DivisionByZero as error:
            raise errors.PdfautonupError(
                "Error: A PDF page have a null dimension."
            ) from error
        return self.Grid(
            cell_number,
            target_size,
            self._margins(target_size, source_size, cell_number),
            self._gaps(target_size, source_size, cell_number),
        )

    def cell_topleft(self, num):
        # pylint: disable=line-too-long
        width, __height = self.grid.cell_number
        return (
            self.grid.margins[0]
            + (self.source_size[0] + self.grid.gaps[0]) * (num % width),
            self.grid.margins[1]
            + (self.source_size[1] + self.grid.gaps[1]) * (num // width),
        )

    @property
    def pages_per_page(self):
        return self.grid.cell_number[0] * self.grid.cell_number[1]


class Panelize(_Layout):
    """Minimum margin is defined, as well as fixed gap."""

    #: Define how the source page will fit into the destination page.
    #: - `margin` is the destination margin (including wasted space);
    #: - `sourcex` is the 'extended' source size (source size, together with gap).
    Grid = namedtuple(
        "Grid", ["margin", "sourcex", "dimension", "target", "pagenumber"]
    )

    def __init__(self, source_size, target_size, arguments):
        # pylint: disable=too-many-arguments
        if arguments.gap[0] is None:
            self.gap = papersize.parse_length("0")
        else:
            self.gap = arguments.gap[0]
        if arguments.margin[0] is None:
            self.margin = papersize.parse_length("0")
        else:
            self.margin = arguments.margin[0]

        if arguments.orientation == "landscape":
            self.grid = self._grid(
                source_size, papersize.rotate(target_size, papersize.LANDSCAPE)
            )
        elif arguments.orientation == "portrait":
            self.grid = self._grid(
                source_size, papersize.rotate(target_size, papersize.PORTRAIT)
            )
        else:
            self.grid = max(
                self._grid(source_size, target_size),
                self._grid(source_size, (target_size[1], target_size[0])),
                key=operator.attrgetter("pagenumber"),
            )

        if self.pages_per_page == 0:
            raise errors.PdfautonupError(
                "Error: Format constraints too tight: Cannot fit any"
                "source page into destination page."
            )

        super().__init__(self.grid.target, arguments)

    def _grid(self, source, target):
        dimension = (
            self._num_fit(target[0], source[0]),
            self._num_fit(target[1], source[1]),
        )

        wasted = (
            self._wasted(target[0], dimension[0], source[0]),
            self._wasted(target[1], dimension[1], source[1]),
        )
        return self.Grid(
            margin=(self.margin + wasted[0], self.margin + wasted[1]),
            sourcex=(source[0] + self.gap, source[1] + self.gap),
            dimension=dimension,
            target=target,
            pagenumber=dimension[0] * dimension[1],
        )

    def _wasted(self, dest, num, source):
        """Return the amount of wasted space

        When fitting `num` elements of size `source` into element of size
        `dest` (in one dimension).
        """
        return (dest - num * (source + self.gap) - 2 * self.margin + self.gap) / 2

    def _num_fit(self, target, source):
        """Return the number of source elements that can fit in target.

        Both `source` and `target` are sizes, in one dimension.
        """
        return int((target - 2 * self.margin + self.gap) // (source + self.gap))

    @property
    def pages_per_page(self):
        return self.grid.dimension[0] * self.grid.dimension[1]

    def cell_topleft(self, num):
        width, __height = self.grid.dimension
        return (
            self.grid.margin[0] + self.grid.sourcex[0] * (num % width),
            self.grid.margin[1] + self.grid.sourcex[1] * (num // width),
        )
