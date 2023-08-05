# -*- coding: utf-8 -*-
# This file is part of hoa-utils.
#
# hoa-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hoa-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hoa-utils.  If not, see <https://www.gnu.org/licenses/>.
#
"""This module defines useful custom types."""
import re
from typing import Union

from hoa.helpers.base import RegexConstrainedString


class string(RegexConstrainedString):
    r"""
    This type represents a 'string' in a HOA file.

    It must match the following regex: '(\\.|[^\\"])*'.
    """

    REGEX = re.compile('(\\.|[^\\"])*')


class integer(RegexConstrainedString):
    """
    This type represents an 'integer' in a HOA file.

    It must match the following regex: "0|[1-9][0-9]*".
    """

    REGEX = re.compile(r"0|[1-9][0-9]*")


class boolean(RegexConstrainedString):
    """
    This type represents a 'boolean' in a HOA file.

    It must match the following regex: "[tf]".
    """

    REGEX = re.compile("[tf]")


class identifier(RegexConstrainedString):
    """
    This type represents an 'integer' in a HOA file.

    It must match the following regex: "[a-zA-Z_][0-9a-zA-Z_-]*".
    """

    REGEX = re.compile("[a-zA-Z_][0-9a-zA-Z_-]*")


class alias(RegexConstrainedString):
    """
    This type represents an 'alias' in a HOA file.

    It must match the following regex: "@[0-9a-zA-Z_-]+".
    """

    REGEX = re.compile("@[0-9a-zA-Z_-]+")


class headername(RegexConstrainedString):
    """
    This type represents a 'headername' in a HOA file.

    It must match the following regex: "[a-zA-Z_][0-9a-zA-Z_-]*".
    """

    REGEX = re.compile("[a-zA-Z_][0-9a-zA-Z_-]*")


class hoa_header_value(RegexConstrainedString):
    """
    This type represents a headername value in a HOA file.

    It must match (BOOLEAN|INT|STRING|IDENTIFIER)
    """

    REGEX = re.compile(
        f"({boolean.REGEX.pattern}|{integer.REGEX.pattern}|{string.REGEX.pattern}|{identifier.REGEX.pattern})"
    )

    @staticmethod
    def to_header_value(value: "hoa_header_value") -> "HEADER_VALUES":
        """
        Convert a HOA header value string to a Python object.

        :param s: the HOA header value string.
        :return: the header value.
        """
        # from the stricter to the looser
        s = str(value)
        if re.match(boolean.REGEX, s):
            return bool(s)
        if re.match(integer.REGEX, s):
            return int(s)
        if re.match(identifier.REGEX, s):
            return identifier(s)
        if re.match(string.REGEX, s):
            return string(s)
        raise ValueError(f"Cannot parse headername value {s}")

    @staticmethod
    def to_hoa_header_value(v: "HEADER_VALUES") -> "hoa_header_value":
        """
        Convert a header value to its HOA header value string.

        :param v: the header value.
        :return: the HOA header value string.
        """
        if isinstance(v, bool):
            return hoa_header_value("t" if v else "f")
        if isinstance(v, int):
            return hoa_header_value(str(v))
        try:
            return hoa_header_value(v)
        except Exception as e:
            raise ValueError(f"Cannot convert value {v}: {str(e)}")


class proposition(RegexConstrainedString):
    """
    This type represents a 'proposition' in a HOA file.

    It must match (BOOLEAN|INT|ANAME)
    """

    REGEX = re.compile(f"({boolean.REGEX}|{integer.REGEX}|{alias.REGEX})")


class acceptance_parameter(RegexConstrainedString):
    """
    This type represents an 'acceptance parameter' in a HOA file.

    It must match (IDENTIFIER | INT)
    """

    REGEX = re.compile(
        f"({boolean.REGEX.pattern}|{identifier.REGEX.pattern}|{integer.REGEX.pattern})"
    )

    @staticmethod
    def to_parameter_value(value: "hoa_header_value") -> "ACCEPTANCE_PARAMETER":
        """
        Convert a HOA acceptance parameter string to a Python object.

        :param s: the HOA acceptance parameter string.
        :return: the parameter value.
        """
        # from the stricter to the looser
        s = str(value)
        if re.match(boolean.REGEX, s):
            return bool(s)
        if re.match(integer.REGEX, s):
            return int(s)
        if re.match(identifier.REGEX, s):
            return identifier(s)
        raise ValueError(f"Cannot parse headername value {s}")

    @staticmethod
    def to_acceptance_parameter(v: "ACCEPTANCE_PARAMETER") -> "acceptance_parameter":
        """
        Convert an acceptance parameter to its HOA header value string.

        :param v: the header value.
        :return: the HOA header value string.
        """
        if isinstance(v, bool):
            return acceptance_parameter("t" if v else "f")
        if isinstance(v, int):
            return acceptance_parameter(str(v))
        try:
            return acceptance_parameter(v)
        except Exception as e:
            raise ValueError(f"Cannot convert value {v}: {str(e)}")


HEADER_VALUES = Union[bool, int, string, identifier]
ACCEPTANCE_PARAMETER = Union[bool, int, identifier]
