.. SPDX-License-Identifier: Apache-2.0
   SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Ballparker contributors

Introduction to Ballparker
--------------------------

.. automodule:: ballparker

An "estimate" is just a recursive structure of :class:`~types.Task` objects, for
which there is an embedded domain-specific language available in this package:
see :mod:`ballparker.dsl`. The main export/viewing functionality is a
configurable conversion to Markdown: see :meth:`~types.Task.as_markdown`.

Ballpark Process
================

Start with just a :func:`~dsl.project` with a list of strings, one for each main
high-level task. The :func:`~dsl.project` call creates a top-level "task" in the
Ballparker model.

Share this out (as source and/or Markdown, depending on audience) and get feedback.

Then, assign each one a "t-shirt size": :const:`~dsl.XS`, :const:`~dsl.S`,
:const:`~dsl.M`, :const:`~dsl.L`, or :const:`~dsl.XL`. With Ballparker, you do
this by turning each string into a (string, size) tuple. Any tasks that are not
given a size are considered :const:`~dsl.UNKNOWN` and can be handled by all
functionality, including adding "uncertainty" (in the form of an inequality) to
parent task point estimates.

Share this out and get feedback.

Then, subdivide (at least) any tasks that are :const:`~dsl.L` or
:const:`~dsl.XL`. In Ballparker's DSL, you replace them with a
:func:`~dsl.grouping` (that is, ``grouping("task description", ...)``) with the
sub-tasks enumerated. Ballparker will automatically sum up the story points of
sub-tasks.

Any uncertainty (leaf tasks with no size mentioned) will be maintained as the
sizes are summed, by reporting the parent's size as ">" the known size.

.. _template:

Ballpark Template
=================

This is available in the Ballparker source tree as
:source:`ballpark_template.py`, or may be downloaded here:
:download:`../ballpark_template.py`.

.. literalinclude:: ../ballpark_template.py

