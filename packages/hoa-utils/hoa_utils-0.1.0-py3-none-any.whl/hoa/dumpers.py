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

"""This module contains utilities to dump the HOA objects."""
from functools import singledispatch
from typing import TextIO

from hoa.ast.acceptance import nb_accepting_sets
from hoa.core import Edge, HOA, HOABody, HOAHeader, State
from hoa.printers import acceptance_condition_to_string, label_expression_to_string
from hoa.types import acceptance_parameter, hoa_header_value


def dump(hoa: HOA, fp: TextIO) -> None:
    """
    Dump the data to a file.

    :param hoa: the HOA object.
    :param fp: the file pointer.
    :return: None.
    """
    fp.write(dumps(hoa))


@singledispatch
def dumps(obj):
    """
    Dump the data into a string in HOA format.

    :param obj: the HOA object.
    :return: the string in HOA format.
    """
    raise ValueError(f"Type {type(obj)} not expected.")


@dumps.register  # type: ignore
def _(hoa: HOA) -> str:
    """
    Dump the data into a string in HOA format.

    :param hoa: the HOA object.
    :return: the string in HOA format.
    """
    header = dumps(hoa.header)
    body = dumps(hoa.body)
    return header + "--BODY--\n" + body + "--END--"


@dumps.register  # type: ignore
def _(hoa_header: HOAHeader):
    """
    Dump the data into a string in HOA format.

    :param hoa_header: the HOA header.
    :return: the string in HOA format.
    """
    s = "HOA: {}\n".format(hoa_header.format_version)
    if hoa_header.nb_states is not None:
        s += "States: {}\n".format(hoa_header.nb_states)
    if hoa_header.start_states is not None:
        s += (
            "\n".join(
                "Start: {}".format(" & ".join(map(str, start_state_set)))
                for start_state_set in hoa_header.start_states
            )
            + "\n"
        )
    if hoa_header.propositions is not None and len(hoa_header.propositions) > 0:
        propositions_string = '"' + '" "'.join(p for p in hoa_header.propositions) + '"'
        s += "AP: {nb} {prop}\n".format(
            nb=len(hoa_header.propositions), prop=propositions_string
        )
    if hoa_header.aliases is not None and len(hoa_header.aliases) > 0:
        s += (
            "\n".join(
                [
                    "Alias: {} {}".format(
                        alias_label.alias,
                        label_expression_to_string(alias_label.expression),
                    )
                    for alias_label in hoa_header.aliases
                ]
            )
            + "\n"
        )
    acceptance_str = acceptance_condition_to_string(hoa_header.acceptance.condition)
    nb_accepting_sets_ = nb_accepting_sets(hoa_header.acceptance.condition)
    s += f"Acceptance: {nb_accepting_sets_} {acceptance_str}\n"
    if hoa_header.acceptance.name is not None:
        s += "acc-name: {} {}\n".format(
            hoa_header.acceptance.name,
            " ".join(
                map(
                    acceptance_parameter.to_acceptance_parameter,
                    hoa_header.acceptance.parameters,
                )
            ),
        )
    if hoa_header.tool is not None:
        s += "tool: {}\n".format(" ".join(hoa_header.tool))
    if hoa_header.name is not None:
        s += 'name: "{}"\n'.format(hoa_header.name)
    if hoa_header.properties is not None and len(hoa_header.properties) > 0:
        s += "properties: {}\n".format(" ".join(hoa_header.properties))
    if hoa_header.headernames is not None and len(hoa_header.headernames) > 0:
        s += (
            "\n".join(
                [
                    "{}: {}".format(
                        key, " ".join(map(hoa_header_value.to_hoa_header_value, values))
                    )
                    for key, values in hoa_header.headernames.items()
                ]
            )
            + "\n"
        )

    return s


@dumps.register  # type: ignore
def _(hoa_body: HOABody):
    """
    Dump the data into a string in HOA format.

    :param hoa_body: the HOA body.
    :return: the string in HOA format.
    """
    return (
        "\n".join(
            [
                dumps(state) + "\n" + "\n".join(map(dumps, edges))
                for state, edges in hoa_body.state2edges.items()
            ]
        )
        + "\n"
    )


@dumps.register  # type: ignore
def _(state: State) -> str:
    """Get the HOA format representation of the state."""
    s = "State: "
    if state.label is not None:
        s += "[" + label_expression_to_string(state.label) + "]" + " "
    s += str(state.index) + " "
    if state.name is not None:
        s += '"' + state.name + '"' + " "
    if state.acc_sig is not None:
        s += "{" + " ".join(map(str, state.acc_sig)) + "}"
    return s


@dumps.register  # type: ignore
def _(edge: Edge) -> str:
    """Get the HOA format representation of the edge."""
    s = ""
    if edge.label is not None:
        s += "[" + label_expression_to_string(edge.label) + "]" + " "
    s += "&".join(map(str, edge.state_conj)) + " "
    if edge.acc_sig is not None:
        s += "{" + " ".join(map(str, edge.acc_sig)) + "}"
    return s
