# pylint: disable=invalid-name
# Requires Python 3.8+
# Ref: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""Configuration for the Sphinx documentation generator."""

import os
from functools import partial
from pathlib import Path

from setuptools_scm import get_version


# -- Path setup --------------------------------------------------------------

PROJECT_ROOT_DIR = Path(__file__).parents[1].resolve()
IS_RELEASE_ON_RTD = (
    os.getenv('READTHEDOCS', 'False') == 'True'
    and os.environ['READTHEDOCS_VERSION_TYPE'] == 'tag'
)
if IS_RELEASE_ON_RTD:
    tags.add('is_release')  # noqa: F821

get_scm_version = partial(get_version, root=PROJECT_ROOT_DIR)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute.


# -- Project information -----------------------------------------------------

github_url = 'https://github.com'
github_repo_org = 'ansible'
github_repo_name = 'pylibssh'
github_repo_slug = f'{github_repo_org}/{github_repo_name}'
github_repo_url = f'{github_url}/{github_repo_slug}'
github_sponsors_url = f'{github_url}/sponsors'

project = f'{github_repo_org}-{github_repo_name}'
author = 'Ansible, Inc.'
copyright = f'2020, {author}'  # noqa: WPS125

# The short X.Y version
version = '.'.join(
    get_scm_version(
        local_scheme='no-local-version',
    ).split('.')[:3],
)

# The full version, including alpha/beta/rc tags
release = get_scm_version()

rst_epilog = f"""
.. |project| replace:: {project}
"""  # pylint: disable=invalid-name


# -- General configuration ---------------------------------------------------

# Ref: python-attrs/attrs#571
default_role = 'any'

nitpicky = True
nitpick_ignore = [
    ('envvar', 'PATH'),
    ('envvar', 'TMPDIR'),
]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',  # autocreate section targets for refs
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    # 'sphinxcontrib.apidoc',
    'sphinxcontrib.towncrier',  # provides `towncrier-draft-entries` directive
    'myst_parser',  # extended markdown; https://pypi.org/project/myst-parser/
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'changelog-fragments/**',  # Towncrier-managed change notes
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_ansible_theme'

html_theme_options = {
    'collapse_navigation': False,
    'analytics_id': '',
    'style_nav_header_background': '#5bbdbf',
    'style_external_links': True,
    'canonical_url': 'https://ansible-pylibssh.readthedocs.io/en/latest/',
    'vcs_pageview_mode': 'edit',
    'navigation_depth': 3,
}

html_context = {
    'display_github': True,
    'github_user': 'ansible',
    'github_repo': 'pylibssh',
    'github_version': 'devel/docs/',
    'current_version': version,
    'latest_version': 'latest',
    'available_versions': ('latest',),
    'css_files': [],  # https://github.com/sphinx-doc/sphinx/issues/8889
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'


# -- Extension configuration -------------------------------------------------

# -- Options for extlinks extension ---------------------------------------
extlinks = {
    'issue': (f'{github_repo_url}/issues/%s', '#%s'),  # noqa: WPS323
    'pr': (f'{github_repo_url}/pull/%s', 'PR #%s'),  # noqa: WPS323
    'commit': (f'{github_repo_url}/commit/%s', '%s'),  # noqa: WPS323
    'gh': (f'{github_url}/%s', 'GitHub: %s'),  # noqa: WPS323
    'user': (f'{github_sponsors_url}/%s', '@%s'),  # noqa: WPS323
}

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'cython': ('https://cython.readthedocs.io/en/latest', None),
    'packaging': ('https://packaging.python.org', None),
    'pip': ('https://pip.pypa.io/en/latest', None),
    'python': ('https://docs.python.org/3', None),
    'python2': ('https://docs.python.org/2', None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for sphinx_tabs extension ---------------------------------------

# Ref:
# * https://github.com/djungelorm/sphinx-tabs/issues/26#issuecomment-422160463
sphinx_tabs_valid_builders = ['linkcheck']  # prevent linkcheck warning

# -- Options for linkcheck builder -------------------------------------------

linkcheck_ignore = [
    r'http://localhost:\d+/',  # local URLs
    r'https://codecov\.io/gh/ansible/pylibssh/branch/devel/graph/badge\.svg',
    r'https://github\.com/ansible/pylibssh/actions',  # 404 if no auth

    # Too many links to GitHub so they cause "429 Client Error:
    # too many requests for url"
    # Ref: https://github.com/sphinx-doc/sphinx/issues/7388
    r'https://github\.com/ansible/pylibssh/issues',
    r'https://github\.com/ansible/pylibssh/pull',
    r'https://github\.com/ansible/ansible/issues',
    r'https://github\.com/ansible/ansible/pull',

    # Requires a more liberal 'Accept: ' HTTP request header:
    # Ref: https://github.com/sphinx-doc/sphinx/issues/7247
    r'https://github\.com/ansible/pylibssh/workflows/[^/]+/badge\.svg',
]
linkcheck_workers = 25

# -- Options for sphinx.ext.autosectionlabel extension -----------------------

# Ref:
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
autosectionlabel_maxdepth = 2  # mitigate Towncrier nested subtitles collision

# -- Options for towncrier_draft extension -----------------------------------

towncrier_draft_autoversion_mode = 'draft'  # or: 'sphinx-version', 'sphinx-release'
towncrier_draft_include_empty = True
towncrier_draft_working_directory = PROJECT_ROOT_DIR
towncrier_draft_config_path = 'pyproject.toml'  # relative to cwd
