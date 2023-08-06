# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydatafaker']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.1.2,<5.0.0',
 'pandas>=1.1.1,<2.0.0',
 'sphinx-rtd-theme>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'pydatafaker',
    'version': '0.1.1a2',
    'description': 'A python package to create fake data with relationships between tables.',
    'long_description': "\n# PyDataFaker\n\nA python package to create fake data with relationships between tables.\n\nCreating fake data can be useful for many different applications. Python\nalready has a great package for creating fake data called Faker\n<https://faker.readthedocs.io/en/master/>. Faker is great for creating\nindividual fake units of data, but it can be time consuming to create\nmore complicated fake data that is actually related to one another.\n\nImagine you are developing a new enterprise resource planning (ERP)\nsoftware to challenge SAP. You may need to create some fake data to test\nyour application. You will need an invoice table, a vendor listing,\npurchase order table, and more. PyDataFaker allows your to quickly\ncreate these tables and generates relationships between them\\!\n\nPyDataFaker is currently under development. At this time it is possible\nto create the following entities:\n\n  - Business: create a fake business with common ERP like tables\n\nMore entities are currently being developed. If you have any ideas of\nadditional entities that should be included please submit an issue here:\n<https://github.com/SamEdwardes/pydatafaker/issues>.\n\n## Table of contents\n\n  - [Installation](#installation)\n  - [Documentation](#documentation)\n  - [Usage](#usage)\n  - [Contributing](#contributing)\n  - [Credits](#credits)\n  - [Reminders for developers](#reminders-for-developers)\n\n## Installation\n\n``` bash\npip install pydatafaker\n```\n\n## Documentation\n\nDocumentation can be found at\n<https://pydatafaker.readthedocs.io/en/latest/index.html>.\n\n## Usage\n\n### Business\n\nGenerate fake business data that could be used to populate an ERP tool.\n\n``` python\nimport pandas as pd\nfrom pydatafaker import business\nbiz =  business.create_business()\n```\n\n`business.create_business()` returns a dictionary containing all of the\nrelated tables.\n\n``` python\nbiz.keys()\n```\n\n    ## dict_keys(['vendor_table', 'po_table', 'invoice_summary_table', 'invoice_line_item_table', 'employee_table', 'contract_table', 'rate_sheet_table', 'timesheet_table'])\n\nEach value inside the dictionary contains a Pandas DataFrame.\n\n``` python\nbiz['invoice_summary_table']\n```\n\n    ##     invoice_id  amount invoice_date     po_id     vendor_id\n    ## 0    inv_00001   85313   2006-05-18  po_00074  vendor_00020\n    ## 1    inv_00002  102511   2010-03-19  po_00017  vendor_00048\n    ## 2    inv_00003  116998   2004-04-04  po_00013  vendor_00006\n    ## 3    inv_00004   91595   2010-03-05  po_00023  vendor_00003\n    ## 4    inv_00005  127056   2014-05-13  po_00060  vendor_00028\n    ## ..         ...     ...          ...       ...           ...\n    ## 245  inv_00246   54936   2018-11-09  po_00071  vendor_00015\n    ## 246  inv_00247   97616   2004-03-25  po_00071  vendor_00015\n    ## 247  inv_00248   98365   2000-09-04  po_00064  vendor_00010\n    ## 248  inv_00249   74361   2005-09-02  po_00052  vendor_00032\n    ## 249  inv_00250   68888   2008-07-07  po_00073  vendor_00097\n    ## \n    ## [250 rows x 5 columns]\n\nTables can be joined together to add additional details.\n\n``` python\ninvoice_summary = biz['invoice_summary_table']\nvendors = biz['vendor_table']\n\npd.merge(invoice_summary, vendors, how='left', on='vendor_id')\n```\n\n    ##     invoice_id  amount  ...                   phone                       email\n    ## 0    inv_00001   85313  ...           (919)472-5788        daniel91@example.com\n    ## 1    inv_00002  102511  ...       (178)697-5211x058    seancastillo@example.org\n    ## 2    inv_00003  116998  ...            932.430.6920     mooreamanda@example.org\n    ## 3    inv_00004   91595  ...        958-198-9444x355      samantha22@example.com\n    ## 4    inv_00005  127056  ...  001-566-535-4000x26384     frankbarron@example.com\n    ## ..         ...     ...  ...                     ...                         ...\n    ## 245  inv_00246   54936  ...       135-151-8494x2791        marvin72@example.org\n    ## 246  inv_00247   97616  ...       135-151-8494x2791        marvin72@example.org\n    ## 247  inv_00248   98365  ...            642-833-5079  dianahernandez@example.net\n    ## 248  inv_00249   74361  ...       (794)308-1258x383     billyvaldez@example.net\n    ## 249  inv_00250   68888  ...   001-291-455-4032x9171    adamsjasmine@example.com\n    ## \n    ## [250 rows x 10 columns]\n\n## Contributing\n\nPlease see [docs/source/contributing.rst](docs/source/contributing.rst).\n\n## Credits\n\nDeveloped by:\n\n  - Sam Edwardes\n\nLogo:\n\n  - Icon made by [Freepik](https://www.flaticon.com/authors/freepik)\n    from [www.flaticon.com](https://www.flaticon.com/)\n  - Front from\n    [fontmeme.com/retro-fonts/](https://fontmeme.com/retro-fonts/)\n  - Logo generated using [logomakr.com](logomakr.com/7scB4)\n",
    'author': 'Sam Edwardes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/pydatafaker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
