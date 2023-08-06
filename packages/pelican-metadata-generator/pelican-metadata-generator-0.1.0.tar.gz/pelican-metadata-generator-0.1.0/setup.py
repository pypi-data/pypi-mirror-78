# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pelican_metadata_generator']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.0,<6.0.0', 'python-slugify>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['pelican-metadata-generator = '
                     'pelican_metadata_generator.cli:main']}

setup_kwargs = {
    'name': 'pelican-metadata-generator',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Pelican Metadata Generator \n\nGraphical application that creates Pelican (<http://blog.getpelican.com/>)\npost metadata. Written in Python 3.x and Qt 5.x (PyQt). Works on Linux,\nWindows and Mac.\n\n![Sample screenshot](screenshot.png)\n\n## Rationale\n\nPelican is static website generator that does not provide any way of\naccessing existing content at new page creation. Simple typo in category \nname or tag name will create spurious entity that you might not catch in \ntime and push to live site.\n\nThis application tries to prevent these mistakes from happening by \nexposing existing Pelican data in graphical user interface. Re-using\nprevious name is as easy as picking it up from GUI. Creation of new\ncategories or tags must be opted-in.\n\nAdded value is that slug will be generated automatically from post title\nand will serve as post file name, if you decide to save data on disk.\n\n## Dependencies\n\n- Python 3.x <https://www.python.org/>\n- PyQt5 <https://www.riverbankcomputing.com/software/pyqt/intro> | <https://pypi.python.org/pypi/PyQt5>\n- slugify <https://pypi.python.org/pypi/PyQt5> | <https://pypi.python.org/pypi/python-slugify>\n\n## Installation (Windows)\n\n- Download and install Python 3 Miniconda from <https://conda.io/miniconda.html>\n- Open command prompt (`cmd.exe`) and run following commands:\n      conda create -n pmg python=3\n      activate pmg\n      pip install python-slugify PyQt5\n- Download this repository\n\nTo run application:\n- Open command prompt (`cmd.exe`)\n- Run `activate pmg`\n- Run `<path_to_repository>/pelican-metadata-generator.py -d <path_to_pelican_content_dir>`\n\n## Adding to menu (Linux only)\n\nCopy `pelican-metadata-generator.desktop` file into \n`$HOME/.local/share/applications/`. If you haven\'t put executable\nsomewhere in `$PATH`, modify `Exec=` line to include absolute path.\nYou probably also want to specify location of your Pelican content.\n\nIf you want your menu entry to have an icon, first you must obtain it.\nThere don\'t seem to be any "official" icon in Pelican sources. Personally,\nI have used image from [@getpelican Twitter account](https://twitter.com/getpelican).\nThen, modify `Icon=` line to provide absolute path to icon on your disk.\n\nYou might need to refresh menu database for your desktop environment\nto pick up changes. KDE SC 4 users may use `kbuildsycoca4`.\n\n## Copying\n\nDistributed under GNU AGPLv3, the same as Pelican. See LICENSE file.\n',
    'author': 'Mirek Długosz',
    'author_email': 'mirek@mirekdlugosz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mirekdlugosz/pelican-metadata-generator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
