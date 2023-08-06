# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import importlib


def read(path, package="gw", file_format=None, skymap=False, **kwargs):
    """Read in a results file.

    Parameters
    ----------
    path: str
        path to results file
    package: str
        the package you wish to use
    file_format: str
        the file format you wish to use. Default None. If None, the read
        function loops through all possible options
    skymap: Bool, optional
        if True, path is the path to a fits file generated with `ligo.skymap`
    **kwargs: dict, optional
        all additional kwargs are passed to the `pesummary.{}.file.read.read`
        function
    """
    if skymap:
        from pesummary.gw.file.skymap import SkyMap

        return SkyMap.from_fits(path)
    module = importlib.import_module("pesummary.{}.file.read".format(package))
    return getattr(module, "read")(path, file_format=file_format, **kwargs)
