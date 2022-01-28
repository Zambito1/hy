# This file is execfile()d with the current directory set to its containing dir.

import re, os, sys, time, html

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.hydomain',
]

from get_version import __version__ as hy_version

# Read the Docs might dirty its checkout, so strip the dirty flag.
hy_version = re.sub(r'[+.]dirty\Z', '', hy_version)

templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

# General information about the project.
project = 'hy'
copyright = '%s the authors' % time.strftime('%Y')

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ".".join(hy_version.split(".")[:-1])
# The full version, including alpha/beta/rc tags.
release = hy_version
hy_descriptive_version = html.escape(hy_version)
if "+" in hy_version:
    hy_descriptive_version += " <strong style='color: red;'>(unstable)</strong>"

exclude_patterns = ['_build', 'coreteam.rst']
add_module_names = True

pygments_style = 'sphinx'

import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_use_smartypants = False
html_show_sphinx = False

html_context = dict(
    hy_descriptive_version = hy_descriptive_version,
    has_active_alpha = True,
)

highlight_language = 'clojure'

intersphinx_mapping = dict(
    py = ('https://docs.python.org/3/', None),
    py3_10 = ('https://docs.python.org/3.10/', None),
    hyrule = ('https://hyrule.readthedocs.io/en/master/', None))
# ** Generate Cheatsheet
import json
from pathlib import Path
from itertools import zip_longest

def refize(spec):
    role = ':hy:func:'
    if isinstance(spec, dict):
        _name = spec['name']
        uri = spec['uri']
        if spec.get('internal'):
            role = ':ref:'
    else:
        uri = spec
        _name = str.split(uri, '.')[-1]
    return '{}`{} <{}>`'.format(role, _name, uri)


def format_refs(refs, indent):
    args = [iter(map(refize, refs))]
    ref_groups = zip_longest(*args, fillvalue="")
    return str.join(
        ' \\\n' + ' ' * (indent + 3),
        [str.join(' ', ref_group) for ref_group in ref_groups],
    )


def format_row(category, divider_loc):
    return '{title: <{width}} | {methods}'.format(
        width=divider_loc,
        title=category['name'],
        methods=format_refs(category['methods'], divider_loc)
    )


def format_table(table_spec):
    table_name = table_spec['name']
    categories = table_spec['categories']
    longest_cat_name = max(len(category['name']) for category in categories)
    table = [
        table_name,
        '-' * len(table_name),
        '',
        '=' * longest_cat_name + ' ' + '=' * 25,
        *(format_row(category, longest_cat_name) for category in categories),
        '=' * longest_cat_name + ' ' + '=' * 25,
        ''
    ]
    return '\n'.join(table)


# Modifications to the cheatsheet should be added in `cheatsheet.json`
cheatsheet_spec = json.loads(Path('./docs/cheatsheet.json').read_text())
cheatsheet = [
    '..',
    '    DO NOT MODIFY THIS FILE. IT IS AUTO GENERATED BY ``conf.py``',
    '    If you need to change or add methods, modify ``cheatsheet_spec`` in ``conf.py``',
    '',
    '.. _cheatsheet:',
    '',
    'Cheatsheet',
    '==========',
    '',
    *map(format_table, cheatsheet_spec),
]
Path('./docs/cheatsheet.rst').write_text('\n'.join(cheatsheet))


# ** Sphinx App Setup


def setup(app):
    app.add_css_file('overrides.css')
