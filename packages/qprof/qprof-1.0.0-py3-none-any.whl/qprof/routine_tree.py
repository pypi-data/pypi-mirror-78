# ======================================================================
# Copyright CERFACS (July 2019)
# Contributor: Adrien Suau (adrien.suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

from collections import Counter
import typing as ty

from qprof.routine import Routine, BaseRoutineWrapper
from qprof._merge_dicts import merge_dict

_flat_profile_header = """Flat profile:

Each sample counts as 0.000001 seconds.
  %   cumulative   self              self     total
 time   seconds   seconds    calls  ms/call  ms/call  name
"""

_flat_profile_footer = """
 %         the percentage of the total running time of the
time       program used by this function.

cumulative a running sum of the number of seconds accounted
 seconds   for by this function and those listed above it.

 self      the number of seconds accounted for by this
seconds    function alone.  This is the major sort for this
           listing.

calls      the number of times this function was invoked, if
           this function is profiled, else blank.

 self      the average number of milliseconds spent in this
ms/call    function per call, if this function is profiled,
           else blank.

 total     the average number of milliseconds spent in this
ms/call    function and its descendents per call, if this
           function is profiled, else blank.

name       the name of the function.  This is the minor sort
           for this listing. The index shows the location of
           the function in the gprof listing. If the index is
           in parenthesis it shows where it would appear in
           the gprof listing if it were to be printed.
\f"""

_copyright = """
Copyright (C) 2012-2016 Free Software Foundation, Inc.
Copyright (C) 2019 Adrien Suau
Copyright (C) 2019 CERFACS

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.
\f"""

_call_graph_header = """             Call graph (explanation follows)


granularity: each sample hit covers 2 byte(s) for 20.00% of 0.05 seconds

index % time    self  children    called     name
"""

_call_graph_footer = """
 This table describes the call tree of the program, and was sorted by
 the total amount of time spent in each function and its children.

 Each entry in this table consists of several lines.  The line with the
 index number at the left hand margin lists the current function.
 The lines above it list the functions that called this function,
 and the lines below it list the functions this one called.
 This line lists:
     index      A unique number given to each element of the table.
                Index numbers are sorted numerically.
                The index number is printed next to every function name so
                it is easier to look up where the function is in the table.

     % time     This is the percentage of the `total' time that was spent
                in this function and its children.  Note that due to
                different viewpoints, functions excluded by options, etc,
                these numbers will NOT add up to 100%.

     self       This is the total amount of time spent in this function.

     children   This is the total amount of time propagated into this
                function by its children.

     called     This is the number of times the function was called.
                If the function called itself recursively, the number
                only includes non-recursive calls, and is followed by
                a `+' and the number of recursive calls.

     name       The name of the current function.  The index number is
                printed after it.  If the function is a member of a
                cycle, the cycle number is printed between the
                function's name and the index number.


 For the function's parents, the fields have the following meanings:

     self       This is the amount of time that was propagated directly
                from the function into this parent.

     children   This is the amount of time that was propagated from
                the function's children into this parent.

     called     This is the number of times this parent called the
                function `/' the total number of times the function
                was called.  Recursive calls to the function are not
                included in the number after the `/'.

     name       This is the name of the parent.  The parent's index
                number is printed after it.  If the parent is a
                member of a cycle, the cycle number is printed between
                the name and the index number.

 If the parents of the function cannot be determined, the word
 `<spontaneous>' is printed in the `name' field, and all the other
 fields are blank.

 For the function's children, the fields have the following meanings:

     self       This is the amount of time that was propagated directly
                from the child into the function.

     children   This is the amount of time that was propagated from the
                child's children to the function.

     called     This is the number of times the function called
                this child `/' the total number of times the child
                was called.  Recursive calls by the child are not
                listed in the number after the `/'.

     name       This is the name of the child.  The child's index
                number is printed after it.  If the child is a
                member of a cycle, the cycle number is printed
                between the name and the index number.

 If there are any cycles (circles) in the call graph, there is an
 entry for the cycle-as-a-whole.  This entry shows who called the
 cycle (as parents) and the members of the cycle (as children.)
 The `+' recursive calls entry shows the number of function calls that
 were internal to the cycle, and the calls entry for each member shows,
 for that member, how many times it was called from other members of
 the cycle.
\f"""


class RoutineTree:
    def __init__(self, main_routine, gate_times: dict, **framework_kwargs):
        self._factory = RoutineNodeFactory()
        self._root = self._factory.get(
            Routine(main_routine, **framework_kwargs), gate_times
        )
        self._total_time = self._root.self_time + self._root.subroutines_times

        self._routines_data = dict()
        self._root.first_pass_routines_data("<spontaneous>", self._routines_data)

    def generate_flat_profile(self, seconds_scale: float = 1.0) -> str:

        format_string = (
            "{0:>6.2f} {1:>9.2f} {2:>8.2f} {3:>8} {4:>8.2f} {5:>8.2f}  {6:<}"
        )

        routines_data = [
            [
                100 * rout_data["self_nano_seconds"] / self._total_time,
                0.0,
                seconds_scale * rout_data["self_nano_seconds"] / 10 ** 9,
                rout_data["self_calls"],
                (seconds_scale * rout_data["self_nano_seconds"] / 10 ** 6)
                / rout_data["self_calls"],
                seconds_scale
                * (
                    rout_data["self_nano_seconds"]
                    + rout_data["subroutines_nano_seconds"]
                )
                / 10 ** 6
                / rout_data["self_calls"],
                rout_name,
            ]
            for rout_name, rout_data in self._routines_data["routines_data"].items()
        ]
        # First sort by name
        routines_data.sort(key=lambda e: e[6])
        # Then sort by decreasing number of calls
        routines_data.sort(key=lambda e: e[3], reverse=True)
        # Finally sort by decreasing runtime
        routines_data.sort(key=lambda e: e[2], reverse=True)
        # Compute the cumulative seconds field
        routines_data[0][1] = routines_data[0][2]
        for i in range(1, len(routines_data)):
            routines_data[i][1] = routines_data[i - 1][1] + routines_data[i][2]

        data_str = "\n".join(format_string.format(*data) for data in routines_data)

        return _flat_profile_header + data_str + _flat_profile_footer + _copyright

    def _get_data(
        self,
        key: str,
        routine_data: dict,
        routines_indices: dict,
        seconds_scale: float = 1.0,
    ):
        if key not in routine_data:
            return list()
        data = list()
        all_routines_data = self._routines_data["routines_data"]
        for rout_name, rout_data in routine_data[key].items():
            data.append(
                (
                    seconds_scale * rout_data["self_nano_seconds"] / 10 ** 9,
                    seconds_scale * rout_data["subroutines_nano_seconds"] / 10 ** 9,
                    "{}/{}".format(
                        rout_data["number"],
                        routine_data["self_calls"]
                        if key == "called_by"
                        else all_routines_data[rout_name]["self_calls"],
                    ),
                    "{} [{}]".format(rout_name, routines_indices[rout_name])
                    if rout_name in routines_indices
                    else rout_name,
                )
            )
        # Sort by name, then by decreasing self time
        data.sort(key=lambda e: e[3])
        data.sort(key=lambda e: e[0], reverse=True)
        return data

    def generate_call_graph(self, seconds_scale: float = 1.0) -> str:
        primary_line_format_string = (
            "{0:<5}  {1:>5.1f} {2:>7.2f} {3:^10.2f} {4:^10}   {5:<}"
        )
        secondary_line_format_string = (
            " " * len("index % time ")
        ) + "{0:>7.2f} {1:^10.2f} {2:^10}       {3:<}"
        routines_strings = []
        routines_indices = self._routines_data["indices"]
        for rout_name, rout_data in sorted(
            self._routines_data["routines_data"].items(),
            key=lambda kv: routines_indices[kv[0]],
        ):
            called_by_data = self._get_data(
                "called_by", rout_data, routines_indices, seconds_scale
            )
            calls_data = self._get_data(
                "calls", rout_data, routines_indices, seconds_scale
            )
            called_by_str = "\n".join(
                [
                    secondary_line_format_string.format(*data)
                    if data[3] != "<spontaneous>"
                    else (" " * 49 + "<spontaneous>")
                    for data in called_by_data
                ]
            )
            primary_line_str = primary_line_format_string.format(
                "[{}]".format(routines_indices[rout_name]),
                100
                * (
                    rout_data["self_nano_seconds"]
                    + rout_data["subroutines_nano_seconds"]
                )
                / self._total_time,
                seconds_scale * rout_data["self_nano_seconds"] / 10 ** 9,
                seconds_scale * rout_data["subroutines_nano_seconds"] / 10 ** 9,
                rout_data["self_calls"],
                "{} [{}]".format(rout_name, routines_indices[rout_name]),
            )
            calls_str = "\n".join(
                [secondary_line_format_string.format(*data) for data in calls_data]
            )
            routines_strings.append(
                "\n".join([called_by_str, primary_line_str, calls_str])
            )

        return (
            _call_graph_header
            + "\n-----------------------------------------------\n".join(
                routines_strings
            )
            + "\n-----------------------------------------------\n"
            + _call_graph_footer
            + _copyright
        )

    def generate_index_by_function_names(self) -> str:
        header = """
Index by function name 
       
"""
        routines_indices = self._routines_data["indices"]
        routines_names = sorted(
            self._routines_data["routines_data"], key=lambda k: routines_indices[k]
        )
        left_column_strs = [
            "[{}] {}".format(routines_indices[rout_name], rout_name)
            for rout_name in routines_names[::2]
        ]
        right_column_strs = [
            "[{}] {}".format(routines_indices[rout_name], rout_name)
            for rout_name in routines_names[1::2]
        ]
        max_len_left = max(map(len, left_column_strs))
        format_left_str = "{:<" + str(max_len_left + 1) + "}"
        if len(right_column_strs) != len(left_column_strs):
            right_column_strs.append("")

        return (
            header
            + "\n"
            + "\n".join(
                [
                    format_left_str.format(l) + r
                    for l, r in zip(left_column_strs, right_column_strs)
                ]
            )
        )

    def generate_gprof_output(self, seconds_scale: float = 1.0) -> str:
        return "\n\n".join(
            [
                self.generate_flat_profile(seconds_scale),
                self.generate_call_graph(seconds_scale),
                self.generate_index_by_function_names(),
            ]
        )


class RoutineNode:
    def __init__(
        self,
        routine: BaseRoutineWrapper,
        factory: "RoutineNodeFactory",
        gate_times: dict,
    ):
        self._routine = routine
        self._subroutines = Counter(
            []
            if routine.is_base
            else [factory.get(rout, gate_times) for rout in routine]
        )
        self._calls = dict()
        for item, count in self._subroutines.items():
            self._calls[item] = self._calls.get(item, 0) + count
        self._calls = Counter(self._calls)
        # Computing routine timings
        self.self_time = (
            sum(
                gate_times[r.name.upper()] * count if r.is_base else 0
                for r, count in self._subroutines.items()
            )
            if not self.is_base
            else gate_times[self.name.upper()]
        )
        self.subroutines_times = sum(
            count * (subrout.self_time + subrout.subroutines_times)
            for subrout, count in self._subroutines.items()
            if not subrout.is_base
        )

    @property
    def name(self):
        return "Unknown" if not self._routine.name else self._routine.name

    @property
    def is_base(self):
        return self._routine.is_base

    def first_pass_routines_data(
        self, called_by: str, global_routines_data: dict, number_of_calls: int = 1
    ):
        # Subroutines index
        max_index_global_data = global_routines_data.setdefault("max_index", 0)
        indices_global_data = global_routines_data.setdefault("indices", dict())
        if self.name not in indices_global_data:
            global_routines_data["max_index"] = max_index_global_data + 1
            global_routines_data["indices"][self.name] = max_index_global_data + 1

        # Call graph and routine data
        self_data = {
            "called_by": {
                called_by: {
                    "number": number_of_calls,
                    "self_nano_seconds": number_of_calls * self.self_time,
                    "subroutines_nano_seconds": number_of_calls
                    * self.subroutines_times,
                }
            },
            "self_nano_seconds": number_of_calls * self.self_time,
            "subroutines_nano_seconds": number_of_calls * self.subroutines_times,
            "self_calls": number_of_calls,
        }

        routines_global_data = global_routines_data.setdefault("routines_data", dict())
        current_routine_global_data = routines_global_data.setdefault(self.name, dict())
        routines_global_data[self.name] = merge_dict(
            current_routine_global_data, self_data
        )

        # And recurse in subroutines
        for rout, count in self._subroutines.items():
            rout.first_pass_routines_data(
                self.name, global_routines_data, count * number_of_calls
            )
            call_data = {
                "calls": {
                    rout.name: {
                        "number": count,
                        "self_nano_seconds": count * rout.self_time,
                        "subroutines_nano_seconds": count * rout.subroutines_times,
                    }
                }
            }
            routines_global_data[self.name] = merge_dict(
                routines_global_data[self.name], call_data
            )


class RoutineNodeFactory:
    def __init__(self):
        self._cache: ty.Dict[BaseRoutineWrapper, "RoutineNode"] = dict()

    def get(
        self, routine_wrapper: BaseRoutineWrapper, gate_times: dict,
    ) -> "RoutineNode":
        if routine_wrapper not in self._cache:
            self._cache[routine_wrapper] = RoutineNode(
                routine_wrapper, self, gate_times
            )
        return self._cache[routine_wrapper]


def profile(
    routine, gate_times: dict, second_scale: float = 1.0, **framework_kwargs
) -> str:
    """Profile the given routine.

    :param routine: The routine to profile.
    :param gate_times: A dictionary whose keys are routine names and values are
        the execution time of the associated routine name.
    :param second_scale: A scaling factor for the number of seconds. This factor
        is used to avoid timings of "0.00" because the precision is not sufficient.
        It will just scale all the timings by the given factor.
    :return: a string that is formatted like gprof's output.
    """
    tree = RoutineTree(routine, gate_times, **framework_kwargs)
    return tree.generate_gprof_output(seconds_scale=second_scale)
