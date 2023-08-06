# Copyright 2019-2020, Collabora, Ltd.
# SPDX-License-Identifier: Apache-2.0
"""Connect a ballpark with Phabricator."""

import re

from .types import Task

_PROJECT_DESC = 'project'
_PHID_ATTR_NAME = 'phid'
_TASK_NUM_ATTR_NAME = 'task_num'
_PHAB_FIELDS_ATTR_NAME = 'phab_fields'


def _get_phid(task):
    if hasattr(task, _PHID_ATTR_NAME):
        return getattr(task, _PHID_ATTR_NAME)
    return None


def _get_task_num(task):
    if hasattr(task, _TASK_NUM_ATTR_NAME):
        return getattr(task, _TASK_NUM_ATTR_NAME)
    return None


def _get_phab_fields(task):
    if hasattr(task, _PHAB_FIELDS_ATTR_NAME):
        return getattr(task, _PHAB_FIELDS_ATTR_NAME)
    return None


def _make_transactions(d):
    """
    Convert a dict of transactions into an actual list of transaction objects.

    Just a convenience function to make the code more concise and less
    repetitive.
    """
    return [
        {
            'type': k,
            'value': v,
        }
        for k, v in d.items()
    ]


class PhabSync:
    """Class to sync some aspects of a ballpark with Phabricator."""

    def __init__(self, project_slug, phab=None):
        """
        Construct object.

        :param project_slug: The project slug, AKA the hashtag without the leading ``#``.
        :param phab: :class:`phabricator.Phabricator` instance (optional)


        If `phab` is not specified, it will be created in the default way, which
        requires ``~/.arcrc`` or ``.arcconfig`` to be populated with a URI and a token.
        """
        self.task_re = re.compile(r'T(?P<task>([1-9][0-9]*)): (?P<title>.*)')
        self.phab = phab
        if self.phab is None:
            from phabricator import Phabricator  # type: ignore

            self.phab = Phabricator()
        self.phab.update_interfaces()
        self.project_slug = project_slug
        results = self.phab.project.search(
            constraints={"slugs": [project_slug]})
        if len(results["data"]) != 1:
            raise RuntimeError(
                "Wrong number of results for project slug search: got "
                + str(len(results["data"]))
            )
        result = results["data"][0]
        self.project_phid = result["phid"]
        self.project_fields = result["fields"]
        self.space_phid = self.project_fields['spacePHID']

    def query_tasks(self, root_task):
        """
        Initialize extra members of the provided task and its children.

        If a task description is of the form ``"T{task_num}: {desc}"``, it
        extracts the task num and sets it as a member of the task.

        Then, for all tasks with a `task_num` member but either no `phid` member
        or no `phab_fields` member, query Phabricator to retrieve all that data.

        Can be run multiple times on the same ballpark without harm.
        """
        def extract_task_num_visitor(task, parent=None):
            if task.is_project:
                return

            if _get_task_num(task) is None:
                m = self.task_re.match(task.description)
                if m:
                    setattr(task, _TASK_NUM_ATTR_NAME,
                            int(m.group('task')))

        root_task.apply_visitor(extract_task_num_visitor)

        # Record which task numbers need to have a query performed
        task_nums = []

        def accumulate_nums_visitor(task, parent=None):
            if _get_task_num(task) is None:
                # Don't have anything to lookup
                return
            if _get_phab_fields(task) is None or _get_phid(task) is None:
                task_nums.append(_get_task_num(task))
        root_task.apply_visitor(accumulate_nums_visitor)

        if not task_nums:
            # Nothing to query
            return

        # Do the query and manipulate the data so it can be more easily used.
        results = self.phab.maniphest.search(constraints={'ids': task_nums})
        data_by_task_num = {x['id']: x['fields'] for x in results['data']}
        phid_by_task_num = {x['id']: x['phid'] for x in results['data']}

        # This shouldn't be empty
        assert(data_by_task_num)

        # Use query results to populate members of tasks.
        def populate_data_visitor(task, parent=None):
            task_num = _get_task_num(task)
            # no known task num
            if task_num is None:
                return

            # not included in query
            if task_num not in phid_by_task_num:
                return

            # populate members
            setattr(task, _PHID_ATTR_NAME, phid_by_task_num[task_num])
            setattr(task, _PHAB_FIELDS_ATTR_NAME,
                    data_by_task_num[task_num])
        root_task.apply_visitor(populate_data_visitor)

    def create_tasks(self, root_task: Task):
        """
        Create Phabricator tasks for each task that lacks one.

        The task number gets added to the task description: you should output
        ``root_task.to_dsl()`` after this (see
        :meth:`ballparker.types.Task.to_dsl`) and update your ballpark
        definition.

        You can run this more than once in a single execution, but don't run it
        in a second execution unless you've updated your ballpark from
        :meth:`~ballparker.types.Task.to_dsl` or you'll create duplicate tasks.

        Tasks that are top-level below :func:`~ballparker.dsl.project` are
        considered epics, and named accordingly in Phabricator. Tasks are
        created in the same space as the project, and leaf tasks have their
        "points" set from the ballpark.

        Subtask/parent task relationships are replicated from
        the ballpark to Phabricator.

        Returns the task description of all tasks created.
        """
        # Must query first - calling it repeatedly is harmless.
        self.query_tasks(root_task)

        created = []
        # Record all newly-created phids here.
        new_phids = set()

        # Record phids of tasks with a parent in the ballpark but whose parent
        # did not have a phid at time of creation
        needs_parentage_phids = set()

        # Create tasks for all that don't have one.
        def create_tasks_visitor(task, parent=None):
            if task.is_project:
                return
            if _get_phid(task) is None:
                # Since we already did init, if we have no phid now,
                # we don't have a task now.

                title = task.description
                is_epic = parent and parent.is_project
                if is_epic:
                    title = '[EPIC] ' + title
                transactions = _make_transactions({
                    'title': title,
                    'space': self.space_phid,
                    'projects.set': [self.project_phid]
                })
                if not task.is_grouping:
                    transactions.extend(
                        _make_transactions({
                            'points': task.known_story_points
                        })
                    )
                needs_parent = False
                if not is_epic:
                    assert(parent)
                    parent_phid = _get_phid(parent)
                    if parent_phid is None:
                        needs_parent = True
                    else:
                        transactions.append({
                            'type': 'parents.set',
                            'value': [parent_phid]
                        })

                # Actually perform the creation
                result = self.phab.maniphest.edit(
                    transactions=transactions
                )

                # Extract the parts of the result we care about,
                # and apply them to the task.
                phid = result['object']['phid']
                task_num = result['object']['id']
                setattr(task, _PHID_ATTR_NAME, phid)
                setattr(task, _TASK_NUM_ATTR_NAME, task_num)

                # Decorate task description for persistence of association.
                task.description = f'T{task_num}: {task.description}'

                # Record our results
                new_phids.add(phid)
                created.append(task.description)

                if needs_parent:
                    needs_parentage_phids.add(phid)

        root_task.apply_visitor(create_tasks_visitor)

        # Query again, now that we've populated the task_num and phid
        # members, to populate other members.
        self.query_tasks(root_task)

        if not needs_parentage_phids:
            # If we don't have any parents to go back in and fix up,
            # we're done. This is the usual case.
            return created

        # Fill in any task parents we missed.
        def set_parents_visitor(task, parent=None):
            if task.is_project:
                return
            phid = _get_phid(task)
            if phid is not None and phid in needs_parentage_phids:
                parent_phid = _get_phid(parent)
                result = self.phab.maniphest.edit(
                    objectIdentifier=phid,
                    transactions={
                        'type': 'parents.set',
                        'value': [parent_phid]
                    }
                )
                print("Added parent")
                print(result)

        root_task.apply_visitor(set_parents_visitor)
        return created
