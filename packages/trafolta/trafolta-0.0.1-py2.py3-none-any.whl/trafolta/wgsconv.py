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

import re
import warnings


def string_to_dms(coord):
    """Converts well formed coordinate string to its components.
    Example: 41°24'12.2" -> (41, 24, 12.2)

    :param str coord: coordinate string formatted as <DD°MM'SS.S[E|N]>
    :rtype: (int, int, float)
    """
    match = re.match(r"^\d{1,2}°\d{1,2}\'\d{1,2}(\.\d+)?\"[EN]?$", coord)
    if not match:
        warnings.warn("Argument value <{}> does not match pattern <DD°MM'SS.S\">".format(coord))
        return
    components = re.split(r"[°'\"]+", match.string)
    return int(components[0]), int(components[1]), float(components[2])


def dms_to_string(d, m, s, decimals=2):
    """Converts degrees, minutes and decimal seconds to well formated coordinate string.
    Example: (41, 24, 12.2)-> 41°24'12.2"

    :param int d: degrees
    :param int m: minutes
    :param float s: decimal seconds
    :param int decimals: second's decimals
    :rtype: str
    """
    return "{d:d}°{m:02d}'{s:0{z}.{c}f}\"".format(d=d, m=m, s=s, z=decimals + 3 if decimals > 0 else 2, c=decimals)


def dmm_to_dms(d, mm):
    """Converts degrees and decimal minutes to degrees, minutes and decimal seconds.
    Example: (41, 24.2033) -> (41, 24, 12.2)

    :param int d: degrees
    :param float mm: decimal minutes
    :rtype: (int, int, float)
    """
    m = int(mm)
    s = (mm - m) * 60
    return d, m, s


def dms_to_dmm(d, m, s):
    """Converts degrees, minutes and decimal seconds to degrees and decimal minutes.
    Example: (41, 24, 12.2) -> (41, 24.2033)

    :param int d: degrees
    :param int m: minutes
    :param float s: decimal seconds
    :rtype: str
    """
    return d, m + s / 60


def dd_to_dms(dd):
    """Converts decimal degrees to degrees, minutes and decimal seconds.
    Example: 41.4034 -> (41, 24, 12.2)

    :param float dd: decimal degrees
    :rtype: (int, int, float)
    """
    d = int(dd)
    m = int((dd - d) * 60)
    s = (dd - d - m / 60) * 3600
    return d, m, s


def dms_to_dd(d, m, s):
    """Converts degrees, minutes and decimal seconds to decimal degrees.
    Example: (41, 24, 12.2) -> 41.4034

    :param int d: degrees
    :param int m: minutes
    :param float s: decimal seconds
    :rtype: float
    """
    return d + (m / 60) + (s / 3600)


def dms_to_sex(d, m, s):
    """Converts degrees, minutes and decimal seconds to sexagesimal seconds.
    Example: (41, 24, 12.2) -> 149052.2

    :param int d: degrees
    :param int m: minutes
    :param float s: decimal seconds
    :rtype: float
    """
    return (d * 3600) + (m * 60) + s
