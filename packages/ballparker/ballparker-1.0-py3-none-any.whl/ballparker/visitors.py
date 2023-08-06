# Copyright 2019-2020, Collabora, Ltd.
# SPDX-License-Identifier: Apache-2.0
"""
Miscellaneous visitors to apply to an estimate.

For all of these visitors, given a project task called ``ESTIMATE`` and a visitor
function named ``visitor``, you apply the visitor as follows:

 .. code-block:: python

    ESTIMATE.apply_visitor(visitor)

 .. seealso:

    :meth:`ballparker.types.Task.apply_visitor`
        The method that applies visitors.

"""


def anonymize(task, parent=None):
    r"""
    Visit with a visitor that replaces task descriptions with systematic but anonymous names.

    Replaces each description with a dotted-decimal "item number".

    Useful for sharing test cases, bug reproductions, etc:
    the overall structure of the estimate remains, but the contents
    of each task's description is removed.

    Use like: ``ESTIMATE.apply_visitor(anonymize)``

    >>> from ballparker.dsl import *
    >>> estimate = project(
    ...     "a",
    ...     grouping("b",
    ...              "bc",
    ...              ("bd", S)))
    >>> estimate.apply_visitor(anonymize)
    >>> estimate.to_dsl()
    "project(\n    ('1'),\n    grouping('2',\n            ('2.1'),\n            ('2.2', S)))"
    """
    base_desc = "" if not parent else task.description + '.'
    for i, subtask in enumerate(task.subtasks, 1):
        subtask.description = f'{base_desc}{i}'
