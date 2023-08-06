# Copyright 2019-2020, Collabora, Ltd.
# SPDX-License-Identifier: Apache-2.0
"""Provides the names for the domain-specific language of ballparks."""

from .types import TShirtSizes, Task

# TODO: De-deplicate these docs: they're also in types.py.

XS = TShirtSizes.XS
"""Smallest task possible - about half a day."""

S = TShirtSizes.S
"""Common task size with some interaction (may have to talk to someone, etc.) - about a day."""

M = TShirtSizes.M
"""Common task size, taking about half a week."""

L = TShirtSizes.L
"""
Task size of "half a sprint" (about 1 week).

You will want to split this into finer-grained tasks before finalizing the ballpark.
"""

XL = TShirtSizes.XL
"""
Largest task size, an entire sprint (about two weeks).

You will want to split this into finer-grained tasks before finalizing the ballpark.
"""

DONE = TShirtSizes.DONE
"""Use this as the size when you're tracking an ongoing project with ballparker, and a task is completed."""

UNKNOWN = TShirtSizes.UNKNOWN
"""
This is the default task size if unspecified.

Adds "uncertainty" to the ballpark (doesn't add any points to parent tasks,
but does turn them into an inequality).
"""


def make_task(a):
    """
    Coerce an argument into a :class:`~ballparker.types.Task`.

    This is mainly for use by :func:`grouping` and :func:`project`,
    not for direct use in your ballparks. However, since those two functions
    both process their arguments using this, it is documented separately. You
    can consider each argument to those functions (aside from the `description`
    argument to :func:`grouping`) to be implicitly wrapped in a
    :func:`make_task` call.

    - If the argument is a string or single-element tuple, it becomes a leaf
      task with the string as a description and with unknown (:const:`UNKNOWN`)
      size.
    - If the argument is a two-element tuple, it's treated as a (description,
      size) pair and converted to a :class:`~ballparker.types.Task` with a
      string description and specified size (either a
      :class:`~ballparker.types.TShirtSizes` or a number).
    - If the argument already is a :class:`~ballparker.types.Task` (e.g., using
      :func:`grouping`), no conversion is required, and the argument is returned
      unchanged.

    So, lines with "leaf" tasks can simply be a string or a 2-tuple of string
    and size (number or t-shirt size).
    """
    if isinstance(a, Task):
        return a
    elif isinstance(a, str):
        return Task.make_leaf(description=a, size=TShirtSizes.UNKNOWN)
    elif isinstance(a, tuple) and len(a) == 1:
        return Task.make_leaf(description=a[0], size=TShirtSizes.UNKNOWN)
    elif isinstance(a, tuple) and len(a) == 2:
        desc, sz = a
        return Task.make_leaf(description=desc, size=sz)
    else:
        raise RuntimeError(
            "Gotta give me more structure/metadata than that.")


def _make_tasks(args):
    return [make_task(a) for a in args]


def grouping(description: str, *args):
    r"""
    Make a "grouping" task with description and sub-tasks, but no inherent size.

    :param description: An string description of this grouping
    :param \*args: See below.

    Each additional argument is converted/coerced into a
    :class:`~ballparker.types.Task` using :func:`make_task` and included in the
    list of subtasks.

    Task groupings should start with a ``grouping("group desc",`` line, followed
    by as many tasks (including groupings) as desired, with all remaining
    closing parentheses ``)`` on the last task line, as needed to match the
    opening parentheses.
    """
    return Task.make_grouping(description=description, subtasks=_make_tasks(args))


def project(*args):
    r"""
    Make a top-level "project" grouping - the root task of an estimate.

    :param \*args: See below.

    Each argument is converted/coerced into a :class:`~ballparker.types.Task`
    using :func:`make_task` and included in the list of subtasks.

    A project should start with a line like ``ESTIMATE = project(``, followed by
    as many tasks (including groupings) as desired, with all remaining closing
    parentheses ``)`` on the last task line, as needed to match the opening
    parentheses.
    """
    return Task.make_project(subtasks=_make_tasks(args))


def process_estimate(estimate: Task, fn: str = "output.md", *args, **kwargs):
    r"""
    Output an estimate in Markdown format to screen and a file.

    :param estimate: An estimate (task tree).
    :param fn: Filename to write Markdown-formatted estimate to.
    :param \*args: Any dditional positional arguments are passed to
        :meth:`~ballparker.types.Task.as_markdown`.
    :param \**kwargs: Any additional keyword arguments are passed to
        :meth:`~ballparker.types.Task.as_markdown`.
    """
    from pathlib import Path

    md = estimate.as_markdown(*args, **kwargs)
    print(md)
    with open(fn, "w", encoding="utf-8") as fp:
        fp.write("# Estimate info\n\n")
        fp.write("Exported from {}\n\n".format(Path(__file__).resolve))
        fp.write(md)
        fp.write("\n")

    print("Estimated size:", estimate.size_string)
