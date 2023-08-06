# Copyright 2019-2020, Collabora, Ltd.
# SPDX-License-Identifier: Apache-2.0
"""Tests related to Markdown export."""

from ..dsl import DONE, XS, L, M, S, grouping, project

ESTIMATE = project(
    grouping("a",
             "aa",
             "ab"),
    "b",
    grouping("c",
             ("ca", S),
             ("cb", M),
             grouping("cc",
                      "cca",
                      "ccb"))
)


def test_markdown_default():
    """Test conversion to Markdown."""
    md = ESTIMATE.as_markdown()
    print()
    print(md)
    assert(md.startswith('- project'))
    md_lines = md.rstrip().split('\n')
    assert('  - a (?)' in md_lines)
    assert('    - ca (1)' in md_lines)
    assert('      - cca (?)' in md_lines)
    for line in md_lines:
        # no empty lines
        assert(line)


def test_markdown_size_first():
    """Test conversion to Markdown."""
    md = ESTIMATE.as_markdown(size_first=True)
    print()
    print(md)
    assert(md.startswith('- (> 4) project'))
    md_lines = md.rstrip().split('\n')
    assert('  - (?) a' in md_lines)
    assert('    - (1) ca' in md_lines)
    assert('      - (?) cca' in md_lines)
    for line in md_lines:
        # no empty lines
        assert(line)


def test_markdown_tshirt_sizes():
    """Test conversion to Markdown."""
    md = ESTIMATE.as_markdown(tshirt_sizes=True)
    print()
    print(md)
    assert(md.startswith('- project (> 4)'))
    md_lines = md.rstrip().split('\n')
    assert('  - a (?)' in md_lines)
    assert('    - ca (S)' in md_lines)
    assert('      - cca (UNKNOWN)' in md_lines)
    for line in md_lines:
        # no empty lines
        assert(line)


def test_markdown_size_levels():
    """Test conversion to Markdown."""
    md = ESTIMATE.as_markdown(size_levels=2)
    print()
    print(md)
    assert(md.startswith('- project (> 4)'))
    md_lines = md.rstrip().split('\n')
    assert('  - a (?)' in md_lines)
    assert('    - ca' in md_lines)
    assert('      - cca' in md_lines)
    for line in md_lines:
        # no empty lines
        assert(line)

    md = ESTIMATE.as_markdown(size_levels=2, skip_levels=1)
    print()
    print(md)
    assert(not md.startswith('- project (> 4)'))
    md_lines = md.rstrip().split('\n')
    assert('- a (?)' in md_lines)
    assert('  - ca' in md_lines)
    assert('    - cca' in md_lines)
    for line in md_lines:
        # no empty lines
        assert(line)


def test_markdown_max_levels():
    """Test conversion to Markdown."""
    md = ESTIMATE.as_markdown(max_levels=3)
    print()
    print(md)
    assert(md.startswith('- project (> 4)'))
    md_lines = md.rstrip().split('\n')
    assert('  - a (?)' in md_lines)
    assert('    - ca (1)' in md_lines)
    assert('cca' not in md)
    for line in md_lines:
        # no empty lines
        assert(line)

    md = ESTIMATE.as_markdown(max_levels=3, skip_levels=1)
    print()
    print(md)
    assert(not md.startswith('- project (> 4)'))
    md_lines = md.rstrip().split('\n')
    assert('- a (?)' in md_lines)
    assert('  - ca (1)' in md_lines)
    assert('    - cca (?)' not in md_lines)
    assert('cca' not in md)
    for line in md_lines:
        # no empty lines
        assert(line)


def test_markdown_as_in_template():
    md = ESTIMATE.as_markdown(size_first=True, tshirt_sizes=True)
    print()
    print(md)
    assert(md)

    md = ESTIMATE.as_markdown(tshirt_sizes=False,
                              size_first=True,
                              size_levels=2)
    print()
    print(md)
    assert(md)
