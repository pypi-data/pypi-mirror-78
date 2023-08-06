# Config for Sphinx documentation of Ballparker
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Ballparker contributors

# Documentation builds require the following modules in addition to sphinx:
# recommonmark
# sphinx-autodoc-typehints

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

project = 'Ballparker'
copyright = '2019-2020, Collabora, Ltd. and the Ballparker contributors'
author = 'Ryan Pavlik'

version = '1.0'
release = '1.0.1'

repo = 'https://gitlab.com/ryanpavlik/ballparker'
main_branch = 'main'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'recommonmark',
]

source_suffix = ['.rst', '.md']

master_doc = 'index'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv']

intersphinx_mapping = {'https://docs.python.org/': None}

autodoc_member_order = 'bysource'

extlinks = {
    'source': (f'{repo}/-/blob/{main_branch}/%s', '')
}


def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    module = info['module']
    if not module:
        return None

    if not module.startswith('ballparker'):
        return None

    fn = module.replace('.', '/') + '.py'
    return f'{repo}/-/blob/{main_branch}/{fn}'
