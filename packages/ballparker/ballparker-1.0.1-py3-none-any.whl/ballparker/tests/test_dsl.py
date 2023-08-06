# Copyright 2019-2020, Collabora, Ltd.
# SPDX-License-Identifier: Apache-2.0
"""Tests related to the Ballparker DSL."""

from ..dsl import DONE, XS, S, L, M, XL, grouping, project

from .data import TEST_DATA

DSL_GLOBALS = {
    'project': project,
    'grouping': grouping,
    'XS': XS,
    'S': S,
    'M': M,
    'L': L,
    'XL': XL,
    'DONE': DONE,
}


def test_dsl():
    """Check that we get the expected `story_points_string`."""
    for sample in TEST_DATA:
        assert(sample.estimate.story_points_string == sample.story_points)


def test_to_dsl():
    """Check that `to_dsl()` works correctly and losslessly."""
    for sample in TEST_DATA:
        print(sample.estimate.to_dsl())
        round_tripped = eval(sample.estimate.to_dsl(), DSL_GLOBALS)

        # Be sure that the round-tripped estimate has the same story points
        assert(round_tripped.story_points_string == sample.estimate.story_points_string)

        # Be sure that the round-tripped estimate converts to the same DSL that created it.
        assert(round_tripped.to_dsl() == sample.estimate.to_dsl())
