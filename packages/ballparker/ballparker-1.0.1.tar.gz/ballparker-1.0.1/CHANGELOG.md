# Ballparker Changelog

<!--
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Ballparker contributors
-->

## Ballparker 1.0.1 (2020-09-08)

This release is mostly to package a bug fix in the Markdown export. All users
are encouraged to upgrade.

- Additions
  - Task.as_markdown: Add an optional `max_levels` parameter, to specify the
    maximum depth to traverse into the tree.
    ([!2](https://gitlab.com/ryanpavlik/ballparker/merge_requests/2))
  - Add tests for markdown export, including for export as done in the ballpark
    template.
    ([!4](https://gitlab.com/ryanpavlik/ballparker/merge_requests/4))
- Fixes
  - Fix exception in markdown exporting.
  - Fix phabricator interop.
    ([!3](https://gitlab.com/ryanpavlik/ballparker/merge_requests/3))

## Ballparker 1.0 (1-September-2020)

Initial release.
