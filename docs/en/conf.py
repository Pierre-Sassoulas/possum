# -*- coding: utf-8 -*-
from datetime import datetime
import os
import sys
import sphinx_bootstrap_theme
from django.conf import settings

# if needed, create possum/settings.py
POSSUM = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONF = os.path.join(POSSUM, "possum", "settings.py")
CONF_TEMPLATE = os.path.join(POSSUM, "possum", "settings_production.py")
if not os.path.isfile(CONF):
    import shutil
    shutil.copyfile(CONF_TEMPLATE, CONF)

sys.path.append(POSSUM)
settings.configure()
from version import POSSUM_VERSION

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest',
              'sphinx.ext.inheritance_diagram', 'sphinx.ext.todo',
              'sphinx.ext.coverage']

templates_path = [os.path.join('..', '_templates')]
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'
project = u'Possum'
copyright = u'2008-%d, Possum Software' % datetime.now().year

version = POSSUM_VERSION
release = version

language = 'en'
today_fmt = '%B %d, %Y'
exclude_trees = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None
default_role = 'obj'

pygments_style = 'sphinx'
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
#html_theme_options = {}
html_title = "%s %s" % (project, release)
#html_logo = os.path.join("..", "images", "bandeau-192.png")
html_favicon = os.path.join("..", "_static", "favicon.ico")
html_static_path = [os.path.join('..', '_static')]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'
html_theme_options = {
    'navbar_site_name': "Summary",
    'navbar_links': [
        ("Home", "http://www.possum-software.org", True),
    ],
    'navbar_sidebarrel': True,
    'navbar_pagenav': False,
    'navbar_pagenav_name': "Page",
    'globaltoc_depth': 1,
    'globaltoc_includehidden': "true",
    #'navbar_class': "navbar navbar-inverse",
    'navbar_fixed_top': "false",
    'source_link_position': "nav",
    # Bootswatch (http://bootswatch.com/) theme.
    #'bootswatch_theme': "darkly",
    'bootswatch_theme': "sandstone",
    'bootstrap_version': "3",
}
# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}
html_sidebars = {
    #    '**': ['globaltoc.html', 'searchbox.html', 'openhub.html'],
}
#    '**': ['globaltoc.html', 'localtoc.html', 'searchbox.html'],
#    'using/windows': ['windowssidebar.html', 'searchbox.html'],

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# html_use_modindex = True
html_use_modindex = False
html_show_sourcelink = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'Possumdoc'

# -- Options for LaTeX output --------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
# latex_documents = [
#  ('index', 'Possum.tex', u'Possum Documentation',
#   u'Bonnegent Sébastien', 'manual'),
#]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_use_modindex = True
