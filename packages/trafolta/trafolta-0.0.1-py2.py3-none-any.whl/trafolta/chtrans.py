# coding=utf-8

# MIT License
#
# Copyright (c) 2020 Elias Raymann & Vincent Vega
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Formula:
# https://www.swisstopo.admin.ch/en/maps-data-online/calculation-services.html (see 'Documents & Publications')

from .wgsconv import *


def wgs84_to_lv03(latitude, longitude, altitude=None):
    """Convert WGS84 to LV03.

    :param float latitude: latitude in degrees
    :param float longitude: longitude in degrees
    :param float altitude: altitude
    :rtype: (float, float, float)
    """
    lat_sex = dms_to_sex(*dd_to_dms(dd=latitude))
    lon_sex = dms_to_sex(*dd_to_dms(dd=longitude))

    # Axiliary values
    lat_aux = (lat_sex - 169028.66) / 10000
    lon_aux = (lon_sex - 26782.5) / 10000

    east = \
        600072.37 \
        + 211455.93 * lon_aux \
        - 10938.51 * lon_aux * lat_aux \
        - 0.36 * lon_aux * lat_aux ** 2 \
        - 44.54 * lon_aux ** 3

    north = \
        200147.07 \
        + 308807.95 * lat_aux \
        + 3745.25 * lon_aux ** 2 \
        + 76.63 * lat_aux ** 2 \
        - 194.56 * lon_aux ** 2 * lat_aux \
        + 119.79 * lat_aux ** 3

    height = None if altitude is None else \
        altitude \
        - 49.55 \
        + 2.73 * lon_aux \
        + 6.94 * lat_aux

    return east, north, height


def wgs84_to_lv95(latitude, longitude, altitude=None):
    """Converts WGS84 to LV95.

    :param float latitude: latitude in degrees
    :param float longitude: longitude in degrees
    :param float altitude: altitude
    :rtype: (float, float, float)
    """
    east, north, height = wgs84_to_lv03(latitude, longitude, altitude)
    return east + 2000000, north + 1000000, height


def __to_wgs84(e_aux, n_aux, height):
    """Helper function to calculate wgs84 from aux values.
    """
    lat = \
        16.9023892 \
        + 3.238272 * n_aux \
        - 0.270978 * e_aux ** 2 \
        - 0.002528 * n_aux ** 2 \
        - 0.0447 * n_aux * e_aux ** 2 \
        - 0.0140 * n_aux ** 3

    lon = \
        2.6779094 \
        + 4.728982 * e_aux \
        + 0.791484 * e_aux * n_aux \
        + 0.1306 * e_aux * n_aux ** 2 \
        - 0.0436 * e_aux ** 3

    alt = None if height is None else \
        height \
        + 49.55 \
        - 12.60 * e_aux \
        - 22.64 * n_aux

    # convert seconds to decimal degrees
    return lat / 0.36, lon / 0.36, alt


def lv03_to_wgs84(east, north, height=None):
    """Converts LV03 to WGS84.

    :param float east: east
    :param float north: north
    :param float height: height
    :rtype: (float, float, float)
    """
    return __to_wgs84(e_aux=(east - 600000) / 1000000, n_aux=(north - 200000) / 1000000, height=height)


def lv95_to_wgs84(east, north, height=None):
    """Converts LV95 to WGS84.

    :param float east: east
    :param float north: north
    :param float height: height
    :rtype: (float, float, float)
    """
    return __to_wgs84(e_aux=(east - 2600000) / 1000000, n_aux=(north - 1200000) / 1000000, height=height)
