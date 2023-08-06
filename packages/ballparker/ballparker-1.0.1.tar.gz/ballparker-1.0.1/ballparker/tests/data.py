# Copyright 2019-2020, Collabora, Ltd.
# SPDX-License-Identifier: Apache-2.0
"""
Sample data for use in the test suite.

Several of these are real ballparks that have been anonymized with
``estimate.apply_visitor(anonymize)`` (see
:meth:`ballparker.types.Task.apply_visitor` and
:func:`ballparker.visitors.anonymize`) then re-exported to the Ballparker DSL
with ``print(estimate.to_dsl())`` (see :meth:`ballparker.types.Task.to_dsl`).

"""

from ..dsl import DONE, XS, L, M, S, grouping, project
from ..types import Task
import attr


@attr.s
class SampleBallpark:
    """Just a tidy way to hold sample ballparks and their data."""

    estimate: Task = attr.ib()
    story_points: str = attr.ib()


TEST_DATA = [

    # Real, anonymized ballpark used for project tracking: some items completed.
    SampleBallpark(
        story_points="> 18.5",
        estimate=project(
            grouping('1',
                     ('1.1', M),
                     ('1.2', DONE),
                     ('1.3', DONE),
                     ('1.4', M)),
            grouping('2',
                     ('2.1', S),
                     grouping('2.2',
                              ('2.2.1'),
                              grouping('2.2.2',
                                       grouping('2.2.2.1',
                                                ('2.2.2.1.1', DONE),
                                                ('2.2.2.1.2', DONE)),
                                       ('2.2.2.2', S)),
                              grouping('2.2.3',
                                       ('2.2.3.1', S),
                                       ('2.2.3.2', M)))),
            grouping('3',
                     ('3.1', XS),
                     ('3.2')),
            grouping('4',
                     ('4.1', L),
                     ('4.2', S)))
    ),

    # Real, anonymized ballpark
    SampleBallpark(
        story_points="> 12.5",
        estimate=project(
            ('1', S),
            grouping('2',
                     ('2.1', XS)),
            grouping('3',
                     ('3.1', M),
                     ('3.2', S),
                     ('3.3', M),
                     ('3.4', M)),
            grouping('4',
                     ('4.1'),
                     ('4.2')),
            ('5', S))
    ),

    # Sample of the "first step" in the ballpark process
    SampleBallpark(
        story_points="?",
        estimate=project(
            "1",
            "2",
            "3",
            "4"
        )
    ),
]
"""Sample estimates and data for testing purposes."""
