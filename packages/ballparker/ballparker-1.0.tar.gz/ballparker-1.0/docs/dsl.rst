.. SPDX-License-Identifier: Apache-2.0
   SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Ballparker contributors

Domain-Specific Language
------------------------

.. automodule:: ballparker.dsl

The key feature of Ballparker is an embedded domain-specific-language (DSL) for
setting up trees of tasks and their associated estimates for ballparks, and a
task model for their manipulation. Your ballpark's "source file" is just a
Python file, typically defining a single estimate and doing some manipulation
and output when called as ``__main__``.

An "estimate" is just a recursive structure of :class:`ballparker.types.Task`
objects. Some tasks are "groupings" - they have no intrinsic size, and they may
have subtasks. These are created with :func:`grouping` calls, or with a
:func:`project` call, used as the "top-level" grouping. Both of those calls take
any number of additional arguments that are or can be converted into tasks:
other :class:`ballparker.types.Task` instances (like a nested grouping), strings
(which become non-grouping tasks with :const:`UNKNOWN` size), or (string,
tshirt-size-constant or float size) tuples which become non-grouping tasks with
the indicated size. (See :func:`make_task` for details.)

Use via the following is recommended for easier-to-read ballparks:

 .. code-block:: python

    from ballparker.dsl import *

or, especially if you have an over-eager linter, you can be more explicit:


 .. code-block:: python

    from ballparker.dsl import project, grouping, XS, S, M, L, XL, DONE, process_estimate

.. seealso::

   :doc:`introduction`
     Details on the ballpark process using this DSL, including a  template for starting a ballpark script
   
   :source:`ballparker/tests/data.py`
     Test data, which includes several anonymized real-world ballparks.

Groupings
=========

.. autofunction:: ballparker.dsl.project

.. autofunction:: ballparker.dsl.grouping

Creating leaf tasks
===================

.. autofunction:: ballparker.dsl.make_task

T-shirt size constants
======================

The "t-shirt size" constants referred to above are the elements of
:class:`ballparker.types.TShirtSizes`, which are imported into the
:mod:`ballparker.dsl` namespace as follows:

   .. autodata:: XS
   .. autodata:: S
   .. autodata:: M
   .. autodata:: L
   .. autodata:: XL
   .. autodata:: DONE
   .. autodata:: UNKNOWN

Output
======

In addition to :meth:`~ballparker.types.Task.as_markdown` and other properties
and methods of :class:`~ballparker.types.Task`, a general-purpose function is
provided in the DSL module that automates some common uses.

.. autofunction:: ballparker.dsl.process_estimate
