.. SPDX-License-Identifier: Apache-2.0
   SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Ballparker contributors

Phabricator Integration
-----------------------

This is a module providing optional connection between a ballpark and
Phabricator "Maniphest" tasks in a project. Most useful at project start, to
populate the workboard from the ballpark estimate.

To persist association between ballpark tasks and Phabricator tasks, the
description of tasks in Python is modified. However, since the task tree is
defined in your own Python code, we cannot update it for you: please use the
:meth:`ballparker.types.Task.to_dsl` method to retrieve a representation of your
updated tree as Ballparker DSL.

Needs arcanist install and configured:

 .. code-block:: sh

   sudo apt install php-curl
   mkdir -p ~/apps/arcanist  # or other directory of your choice
   cd ~/apps/arcanist
   git clone https://github.com/phacility/libphutil.git
   git clone https://github.com/phacility/arcanist.git
   ln -s ~/apps/arcanist/arcanist/bin/arc ~/.local/bin/
   # or other target directory on your path


Create an `~/.arcrc` file (or `.arcconfig` in current directory) with the
following contents, modified as required:

 .. code-block:: json

   {
     "phabricator.uri": "https://phabricator.example.com/"
   }

then run:

 .. code-block:: sh

   arc install-certificate

and follow the prompts to get a token, etc.

.. note::
   You will need the ``phabricator`` PyPI package installed to use this module.

.. autoclass:: ballparker.phab.PhabSync
   :members:

