# Copyright 2019-2020, Collabora, Ltd.
# SPDX-License-Identifier: Apache-2.0
"""
Define the main types and constants of this package.

To create instances of :class:`Task`, it's recommended to use the DSL in :mod:`ballparker.dsl`.
"""
from enum import Enum
from typing import Callable, List, Optional, Sequence, Union

import attr


class TShirtSizes(Enum):
    """
    So-called "T-shirt size" estimation sizes.

    This is a binning/quantization method of estimation: it is intentionally
    somewhat coarse-grained, to provide fewer choices and thus easier estimation.
    It is based on US T-shirt sizes: rather than a number, there is just
    extra-small, small, medium, large, extra-large, etc. Those five basic ones
    are the ones supported by Ballparker. Rather than directly estimating
    points (days of work), you estimate the kind of work or size category instead.

    Each size is associated with a number of story points as a starting place,
    though the various ways to make a :class:`Task` do accept numbers as
    sizes in addition to :class:`TShirtSizes` if you want to fine-tune.

    These are all imported directly by name into :mod:`ballparker.dsl` for ease of use.
    """

    DONE = 0
    """Use this as the size when you're tracking an ongoing project with ballparker, and a task is completed."""

    XS = 0.5
    """Smallest task possible - about half a day."""

    S = 1
    """Common task size with some interaction (may have to talk to someone, etc.) - about a day."""

    M = 3
    """Common task size, taking about half a week."""

    L = 5
    """
    Task size of "half a sprint" (about 1 week).

    You will want to split this into finer-grained tasks before finalizing the ballpark.
    """

    XL = 10
    """Largest task size, an entire sprint (about two weeks).

    You will want to split this into finer-grained tasks before finalizing the ballpark.
    """

    UNKNOWN = None
    """
    This is the default task size if unspecified.

    Adds "uncertainty" to the ballpark (doesn't add any points to parent tasks,
    but does turn them into an inequality).
    """

    GROUPING = -1
    """
    This is a sentinel value used in groupings, not for manual use.

    It indicates this task has no inherent size of its own, but should instead sum
    up all sub-task sizes.
    """


class _AllLevelsSentinel(Enum):
    ALL_LEVELS = 0


ALL_LEVELS = _AllLevelsSentinel.ALL_LEVELS
"""
Singleton sentinel value to pass to :meth:`Task.as_markdown` as a level number.

If this, instead of a number, is passed as `size_levels` (the default), the `size_levels`
value will be considered to be larger than all levels in the tree, and thus
sizes will be output for all task levels.

If this, instead of a number, is passed as `max_levels`, the `max_levels` value
will be considered to be larger than all levels in the tree, and thus all task
levels will be traversed for output.
"""


def _indent(s, indentation=" " * 8):
    return indentation + s.replace("\n", "\n" + indentation)


@attr.s
class Task:
    """A task with a description and a size or sub-tasks."""

    _PROJECT_DESCRIPTION = 'project'

    description: str = attr.ib()
    """A description of this task/grouping."""

    size: Union[TShirtSizes, int, float] = attr.ib()
    """
    The inherent size of this task.

    Only specified with a valid value for leaf (non-grouping) tasks.
    """

    subtasks: List['Task'] = attr.ib(factory=list)
    """
    A list of sub-tasks for this task.

    Only tasks with no inherent size can have a non-empty list of subtasks.
    """

    def as_markdown(
        self,
        format_task: Optional[Callable[['Task'], str]] = None,
        size_first: bool = False,
        tshirt_sizes: bool = False,
        skip_levels: Optional[int] = None,
        size_levels: Union[int, _AllLevelsSentinel] = ALL_LEVELS,
        max_levels: Union[int, _AllLevelsSentinel] = ALL_LEVELS,
    ) -> str:
        """
        Get this task (and any sub-tasks) as a Markdown document.

        :param format_task: An optional function taking a task and returning a
            string.
        :param size_first: Whether size should come before the description
            instead of after. Only applied if `format_task` is :const:`None`.
        :param tshirt_sizes: Whether sizes should be shown in "T-shirt sizes"
            (see :class:`TShirtSizes`), where available, instead of their
            story-point equivalent.
        :param skip_levels: How many levels of the tree to skip. Most common
            values are 0 (no levels) and 1 (skip the top level, often a
            "project" grouping).
        :param size_levels: How many levels of the tree should have their
            sizes annotated. The sentinel values :const:`ALL_LEVELS` means "all
            levels" (default). Other values may be useful when processing
            output for supplying to customers, for example, to remove the very
            fine-grained estimates at tree leaves.
        :param max_levels: The maximum levels of tasks, starting at the root project,
            that should be traversed and output. Note that if `skip_levels` is not 0,
            the number of levels actually output is less
            (``max_levels - skip_levels``). The sentinel values :const:`ALL_LEVELS` means "all
            levels" (default). Other values may be useful when processing
            output for supplying to customers, for example, to remove the very
            fine-grained tasks at tree leaves.

        :return: Multi-line text suitable for processing as Markdown.
        """
        kwargs = {
            "format_task": format_task,
            "size_first": size_first,
            "tshirt_sizes": tshirt_sizes,
            "skip_levels": skip_levels,
            "size_levels": size_levels,
            "max_levels": max_levels,
        }
        return self._as_markdown_impl(0, kwargs)

    def to_dsl(self) -> str:
        r"""
        Get the equivalent ballpark DSL of this task and any subtasks.

        >>> Task.make_leaf("desc").to_dsl()
        "('desc')"
        >>> Task.make_leaf("desc", TShirtSizes.S).to_dsl()
        "('desc', S)"
        >>> Task.make_leaf("desc", 1).to_dsl()
        "('desc', 1)"
        >>> Task.make_grouping("desc", subtasks=[]).to_dsl()
        "grouping('desc')"
        >>> Task.make_grouping("desc", subtasks=[Task.make_leaf("subtask")]).to_dsl()
        "grouping('desc',\n        ('subtask'))"
        >>> Task.make_project(subtasks=[]).to_dsl()
        'project()'
        >>> Task.make_project(subtasks=[Task.make_leaf("subtask")]).to_dsl()
        "project(\n    ('subtask'))"
        """
        if self.is_grouping:
            if self.description == Task._PROJECT_DESCRIPTION:
                call = "project("
                wrap_immediate = True
                args = []
                indentation = " " * 4
            else:
                call = "grouping("
                wrap_immediate = False
                args = [repr(self.description)]
                indentation = " " * 8  # length of "grouping"
            if self.subtasks:
                args.extend(_indent(x.to_dsl(), indentation=indentation) for x in self.subtasks)
                if wrap_immediate:
                    call = call + '\n'
            return call + ',\n'.join(args) + ')'
        if self.has_unknowns:
            return f"({repr(self.description)})"
        return f"({repr(self.description)}, {self.size_string})"

    def apply_visitor(self, visitor, parent=None) -> None:
        """
        Call the visitor with this task and all sub-tasks recursively.

        The visitor will get a single positional argument (the task)
        and a keyword argument `parent` (which will be None by default
        at the initial task).

        This is a pre-order, depth-first traversal, if you are curious.

        .. seealso::

           :mod:`ballparker.visitors`
               Bundled standalone visitors.

        """
        visitor(self, parent=parent)
        for subtask in self.subtasks:
            subtask.apply_visitor(visitor, parent=self)

    @property
    def size_string(self) -> str:
        """
        Get the size of this task or its recursive sub-tasks.

        Same as :attr:`story_points_string` for groupings. For leaf tasks, this
        returns the t-shirt size estimate instead of the numerical story points,
        where available.

        >>> Task.make_leaf("desc").size_string
        'UNKNOWN'
        >>> Task.make_leaf("desc", TShirtSizes.S).size_string
        'S'
        >>> Task.make_leaf("desc", 1).size_string
        '1'
        >>> Task.make_grouping("desc", subtasks=[]).size_string
        '?'
        >>> Task.make_grouping("desc", subtasks=[Task.make_leaf("subtask")]).size_string
        '?'
        >>> Task.make_project(subtasks=[]).size_string
        '?'
        >>> Task.make_project(subtasks=[Task.make_leaf("subtask", TShirtSizes.S)]).size_string
        '1'
        """
        if self.is_grouping:
            return self.story_points_string

        if isinstance(self.size, TShirtSizes):
            return self.size.name

        if self.has_unknowns:
            return "?"

        return str(self.size)

    @property
    def story_points_string(self) -> str:
        """
        Get a string representation of the numerical story points for this task (or its sub-tasks, recursively).

        String representation allows returning ``"?"`` if no size was provided,
        or ``">"`` and some value if one or more sub-tasks has unknown size.

        >>> Task.make_leaf("desc").story_points_string
        '?'
        >>> Task.make_leaf("desc", TShirtSizes.S).story_points_string
        '1'
        >>> Task.make_leaf("desc", 1).story_points_string
        '1.0'
        >>> Task.make_grouping("desc", subtasks=[]).story_points_string
        '?'
        >>> Task.make_grouping("desc", subtasks=[Task.make_leaf("subtask")]).story_points_string
        '?'
        >>> Task.make_grouping("desc", subtasks=[
        ...     Task.make_leaf("subtask"),
        ...     Task.make_leaf("subtask 2", TShirtSizes.S)]).story_points_string
        '> 1'
        >>> Task.make_project(subtasks=[]).story_points_string
        '?'
        >>> Task.make_project(subtasks=[Task.make_leaf("subtask", TShirtSizes.S)]).story_points_string
        '1'

        >>> from ballparker.dsl import *
        >>> make_task("desc").story_points_string
        '?'
        >>> make_task(("desc", S)).story_points_string
        '1'
        >>> make_task(("desc", 1)).story_points_string
        '1.0'
        >>> grouping("desc").story_points_string
        '?'
        >>> grouping("desc",
        ...         ("subtask")).story_points_string
        '?'
        >>> grouping("desc",
        ...         ("subtask"),
        ...         ("subtask 2", S)).story_points_string
        '> 1'
        >>> project().story_points_string
        '?'
        >>> project(
        ...     ("subtask", S)).story_points_string
        '1'
        """
        known_points = self.known_story_points
        if known_points == 0:
            return "DONE"
        if not known_points:
            return "?"
        if self.has_unknowns:
            return "> {}".format(known_points)
        return "{}".format(known_points)

    @property
    def is_grouping(self) -> bool:
        """
        Check if this task is a grouping.

        A grouping has no inherent size, and may have subtasks.

        >>> Task.make_leaf("desc").is_grouping
        False
        >>> Task.make_leaf("desc", TShirtSizes.S).is_grouping
        False
        >>> Task.make_grouping("desc", subtasks=[]).is_grouping
        True
        >>> Task.make_grouping("desc", subtasks=[Task.make_leaf("subtask")]).is_grouping
        True
        >>> Task.make_project(subtasks=[]).is_grouping
        True
        >>> Task.make_project(subtasks=[Task.make_leaf("subtask")]).is_grouping
        True
        """
        # non-groupings must not have any subtasks.
        if self.size is not TShirtSizes.GROUPING:
            assert(not self.subtasks)
        return self.size is TShirtSizes.GROUPING

    @property
    def is_project(self) -> bool:
        """
        Return True if this is the :func:`~ballparker.dsl.project`-created grouping.

        >>> Task.make_leaf("desc").is_project
        False
        >>> Task.make_leaf("desc", TShirtSizes.S).is_project
        False
        >>> Task.make_grouping("desc", subtasks=[]).is_project
        False
        >>> Task.make_grouping("desc", subtasks=[Task.make_leaf("subtask")]).is_project
        False
        >>> Task.make_project(subtasks=[]).is_project
        True
        >>> Task.make_project(subtasks=[Task.make_leaf("subtask")]).is_project
        True
        """
        return self.description == Task._PROJECT_DESCRIPTION

    @property
    def has_unknowns(self) -> bool:
        """Check if this task or any sub-tasks are missing a size estimate."""
        if self.is_grouping:
            return (not self.subtasks) or (
                True in (x.has_unknowns for x in self.subtasks)
            )
        return self.size == TShirtSizes.UNKNOWN

    @property
    def known_story_points(self) -> Optional[float]:
        """
        Get the number of known story points for this task or its sub-tasks.

        Note that this is usually not as useful for display as
        :attr:`story_points_string`, since that incorporates the uncertainty of
        tasks with unknown size.
        """
        if self.is_grouping:
            if not self.subtasks:
                return None
            points = (x.known_story_points for x in self.subtasks)
            total = sum(x for x in points if x is not None)
            if total == 0:
                if self.has_unknowns:
                    return None
                return 0
            return total
        if self.size in (None, TShirtSizes.GROUPING, TShirtSizes.UNKNOWN):
            return None
        if isinstance(self.size, TShirtSizes):
            return self.size.value
        return float(self.size)

    @classmethod
    def make_leaf(cls, description: str, size: Union[TShirtSizes, float] = TShirtSizes.UNKNOWN) -> 'Task':
        """
        Create a leaf (non-grouping) task.

        Typically invoked by passing additional arguments to the
        :func:`~dsl.grouping` or :func:`~dsl.project` DSL functions.
        """
        if size == TShirtSizes.GROUPING:
            raise RuntimeError(("Cannot use {} as a leaf task's size: " +
                                "sentinel used by project() and grouping() calls.").format(
                size))
        if description == cls._PROJECT_DESCRIPTION:
            raise RuntimeError(
                "Cannot use {} as a task description: sentinel value used by project(...) calls.".format(
                    repr(cls._PROJECT_DESCRIPTION)))
        return cls(description, size)

    @classmethod
    def make_grouping(cls, description: str, subtasks: Sequence['Task']) -> 'Task':
        """
        Create a "grouping" non-leaf task.

        Typically invoked by the :func:`~dsl.grouping` DSL function.
        """
        if description == cls._PROJECT_DESCRIPTION:
            raise RuntimeError(
                "Cannot use {} as a grouping description: sentinel value used by project(...) calls.".format(
                    repr(cls._PROJECT_DESCRIPTION)))
        return cls(description, size=TShirtSizes.GROUPING, subtasks=list(subtasks))

    @classmethod
    def make_project(cls, subtasks: Sequence['Task']) -> 'Task':
        """
        Create a "project" root task.

        Typically invoked by the :func:`~dsl.project` DSL function.
        """
        return cls(cls._PROJECT_DESCRIPTION, size=TShirtSizes.GROUPING, subtasks=list(subtasks))

    def _as_markdown_impl(self, level: int, kwargs):
        format_task = kwargs.get("format_task")
        if format_task is not None:
            formatted = format_task(self)
        else:
            size_levels = kwargs.get("size_levels")
            if size_levels == ALL_LEVELS:
                # Sentinel value, meaning provide size for all levels
                size_levels = level + 1

            if level >= size_levels:
                format_str = "{desc}"
            elif kwargs.get("size_first"):
                format_str = "({size}) {desc}"
            else:
                format_str = "{desc} ({size})"
            formatted = format_str.format(
                size=self.size_string
                if kwargs.get("tshirt_sizes")
                else self.story_points_string,
                desc=self.description,
            )
        max_levels = kwargs["max_levels"]
        if max_levels == ALL_LEVELS:
            # Sentinel value, meaning traverse all levels
            max_levels = level + 2
        skip_levels = 0
        if "skip_levels" in kwargs and isinstance(kwargs["skip_levels"], int):
            skip_levels = kwargs["skip_levels"]
        indent = level - skip_levels
        line = "".join((("  " * indent), "- ", formatted, "\n"))
        if not self.is_grouping:
            return line
        lines = []
        if level >= skip_levels:
            lines.append(line)

        if level + 1 < max_levels:
            lines.extend(x._as_markdown_impl(level + 1, kwargs)
                         for x in self.subtasks)
        return "".join(lines)
