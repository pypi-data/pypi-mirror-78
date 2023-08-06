# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinxawesome_theme']

package_data = \
{'': ['*'], 'sphinxawesome_theme': ['static/*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'sphinx>3',
 'sphinxawesome-sampdirective>=1.0.3,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<2.0.0']}

entry_points = \
{'sphinx.html_themes': ['sphinxawesome_theme = sphinxawesome_theme']}

setup_kwargs = {
    'name': 'sphinxawesome-theme',
    'version': '1.12.0',
    'description': 'An awesome theme for the Sphinx documentation generator',
    'long_description': '====================\nSphinx awesome theme\n====================\n\n.. image:: https://img.shields.io/pypi/l/sphinxawesome-theme?color=blue&style=for-the-badge\n   :target: https://opensource.org/licenses/MIT\n   :alt: MIT license\n\n.. image:: https://img.shields.io/pypi/v/sphinxawesome-theme?style=for-the-badge\n   :target: https://pypi.org/project/sphinxawesome-theme\n   :alt: PyPI package version number\n\n.. image:: https://img.shields.io/netlify/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22?style=for-the-badge\n   :target: https://sphinxawesome.xyz\n   :alt: Netlify Status\n\nThis is an awesome theme for the `Sphinx\n<http://www.sphinx-doc.org/en/master/>`_ documentation generator. See how the theme\nlooks on the `demo page <https://sphinxawesome.xyz>`_.\n\n\n--------\nFeatures\n--------\n\nThe theme includes several usability improvements:\n\n.. features-start\n\nCopy code blocks\n    Code blocks have a **Copy** button, allowing you to copy code snippets to the\n    clipboard.\n\nNew directive for highlighting placeholder variables\n    The theme supports a new directive ``samp``, which is the equivalent of the\n    built-in ``:samp:`` interpreted text role. This allows you to highlight placeholder\n    variables in code blocks.\n\nImproved user experience\n    A lot of small features make the theme more usable. To name a few:\n\n    - You can tab through headlines and captions enabling easy navigation with the\n      keyboard.\n    - You can link to admonitions. Their titles have the same “permalink” mechanism as\n      headlines and captions.\n    - Clicking on the ``#`` icon for permalinks copies the link to the clipboard.\n    - Collapsible navigation menu: All elements are reachable from all pages.\n    - Keyboard shortcut for the search input: ``/``.\n\n.. features-end\n\n------------\nInstallation\n------------\n\nInstall the theme as a Python package:\n\n.. install-start\n\n.. code:: console\n\n   $ pip install sphinxawesome-theme\n\n.. install-end\n\nRead the full `installation instructions\n<https://sphinxawesome.xyz/docs/install.html#how-to-install-the-theme>`_ for more\ninformation.\n\n-----\nUsage\n-----\n\n.. use-start\n\nTo use the theme, set ``html_theme`` in the Sphinx configuration file\n``conf.py``:\n\n.. code:: python\n\n   html_theme = "sphinxawesome_theme"\n\n.. use-end\n\nRead the full `usage information\n<https://sphinxawesome.xyz/docs/use.html#how-to-use-the-theme>`_ for more information.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-theme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
