# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_ags4']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'python-ags4',
    'version': '0.1.4',
    'description': 'A library to read and write AGS4 files using Pandas DataFrames',
    'long_description': "# python-ags4\nA library to read and write AGS4 files using Pandas DataFrames\n\n## Installation\n\n```bash\npip install python-ags4\n```\n\n## Introduction\n`python-ags4` is a library of functions that lets a user import [AGS4](http://www.agsdataformat.com/datatransferv4/intro.php) files to a collection of Pandas DataFrames. The data can be analyzed, manipulated, and updated using Pandas and then exported back to an AGS4 file.\n\n## Examples\n\n#### Import module:\n```python\nfrom python_ags4 import AGS4\n```\n\n#### Import data from an AG4 file:\n```python\ntables, headings = AGS4.AGS4_to_dataframe('/home/asitha/Projects/python-AGS4/tests/test_data.ags')\n```\n* *tables* is a dictionary of Pandas DataFrames. Each DataFrame contains the data from a *GROUP* in the AGS4 file. \n* *headings* is a dictionary of lists. Each list has the header names of the corresponding *GROUP*\n\nAll data are imported as text so they cannot be analyzed or plotted immediately. You can use the following code to convert all the numerical data in a DataFrame from text to numeric.\n\n```python\nLOCA = AGS4.convert_to_numeric(tables['LOCA'])\n```\n\nThe `AGS4.convert_to_numeric()` function automatically converts all columns in the input DataFrame with the a numeric *TYPE* to a float.\n\n#### Export data back to an AGS4 file:\n\n``` python\nAGS4.dataframe_to_AGS4(tables, headings, '/home/asitha/Documents/output.ags')\n```\n",
    'author': 'Asitha Senanayake',
    'author_email': 'asitha.senanayake@utexas.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asitha-sena/python-AGS4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
