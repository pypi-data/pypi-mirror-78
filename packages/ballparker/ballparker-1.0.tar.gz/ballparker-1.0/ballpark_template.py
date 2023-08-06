# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Ballparker contributors
#
# To the extent possible under law, the person who associated CC0 with this work
# has waived all copyright and related or neighboring rights to this work. This
# work is published from: United States.

from ballparker.dsl import *

ESTIMATE = project(
    # List your main high-level tasks here
)

if __name__ == "__main__":
    # This will print a Markdown-formatted version of your ballpark,
    # useful for internal discussion.
    print(ESTIMATE.as_markdown(size_first=True, tshirt_sizes=True))

    # This will print a less detailed, story-point-centric Markdown-formatted version
    # of your ballpark for customers.
    print(ESTIMATE.as_markdown(tshirt_sizes=False,
                               size_first=True,
                               size_levels=2))

    # This will print your estimate as formatted in the Ballparker :mod:`~ballparker.dsl`
    # domain-specific language: you can use this for formatting or for updating your source
    # after programmatic manipulation
    print(ESTIMATE.to_dsl())

    # This will write a Markdown-formatted file with your estimate,
    # as well as show it to screen (standard output) and show an overall duration.
    process_estimate(ESTIMATE)

    # IMPORTANT: Do not forget to add project management overhead (often a fixed percentage) to the estimates
    # developed using Ballparker!
