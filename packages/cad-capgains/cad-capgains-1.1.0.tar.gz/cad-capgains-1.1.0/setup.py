# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['capgains', 'capgains.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.23.0,<3.0.0', 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['capgains = capgains.cli:capgains']}

setup_kwargs = {
    'name': 'cad-capgains',
    'version': '1.1.0',
    'description': 'A CLI tool to calculate your capital gains',
    'long_description': 'Canadian Capital Gains CLI Tool\n=\n[![Build Status](https://travis-ci.org/EmilMaric/cad-capital-gains.svg?branch=master)](https://travis-ci.org/EmilMaric/cad-capital-gains)\n[![codecov](https://codecov.io/gh/EmilMaric/cad-capital-gains/branch/master/graph/badge.svg)](https://codecov.io/gh/EmilMaric/cad-capital-gains)\n\nCalculating your capital gains and tracking your adjusted cost base (ACB) manually, or using an Excel document, often proves to be a laborious process. This CLI tool calculates your capital gains and ACB for you, and just requires a CSV file with basic information about your transactions. The idea with this tool is that you are able to more or less cut-and-copy the output that it genarates and copy it into whatever tax filing software you end up using.\n\n## Noteable features:\n- Supports transactions with multiple different stock tickers in the same CSV file, and outputs them in separate tables.\n- Currently supports transactions done in both USD and CAD. For USD transactions, the daily exchange rate will be automatically fetched from the Bank of Canada.\n- Will automatically apply [superficial capital loss](https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/personal-income/line-127-capital-gains/capital-losses-deductions/what-a-superficial-loss.html) rules when calculating your capital gains and ACB. This tool only supports full superficial capital losses, and does not support partial superficial losses. In sales with a superficial capital loss, the capital loss will be carried forward as perscribed by the CRA. A sale with a capital loss will be treated as superficial if it satisifies the following:\n    - Shares with the same ticker were bought in the 61 day window (30 days before or 30 days after the sale)\n    - There is a non-zero balance of shares sharing the same ticker at the end of the 61 day window (30 days after the sale)\n- Outputs the running adjusted cost base (ACB) for every transaction with a non-superficial capital gain/loss\n\n# Installation\n```bash\n# To get the latest release\npip install cad-capgains\n```\n\n# CSV File Requirements\nTo start, create a CSV file that will contain all of your transactions. In the CSV file, each line will represent a `BUY` or `SELL` transaction.  Your transactions **must be in order**, with the oldest transactions coming first, followed by newer transactions coming later. The format is as follows:\n```csv\n<yyyy-mm-dd>,<transaction_description>,<stock_ticker>,<action(BUY/SELL)>,<quantity>,<price>,<commission>,<currency>\n```\nHere is a sample CSV file:\n```csv\n# sample.csv\n2017-2-15,ESPP PURCHASE,GOOG,BUY,100,50.00,10.00,USD\n2017-5-20,RSU VEST,GOOG,SELL,50,45.00,0.00,CAD\n```\n\n**NOTE: This tool only supports calculating ACB and capital gains with transactions\ndating from May 1, 2007 and onwards.**\n\n# Usage\nTo show the CSV file in a nice tabular format you can run:\n```bash\n$ capgains show sample.csv\n+------------+--------------------+----------+----------+-------+---------+--------------+------------+\n| date       | transaction_type   | ticker   | action   |   qty |   price |   commission |   currency |\n|------------+--------------------+----------+----------+-------+---------+--------------+------------|\n| 2017-02-15 | ESPP PURCHASE      | GOOG     | BUY      |   100 |   50.00 |        10.00 |        USD |\n| 2017-05-20 | RSU VEST           | GOOG     | SELL     |    50 |   45.00 |         0.00 |        CAD |\n+------------+--------------------+----------+----------+-------+---------+--------------+------------+\n```\nTo calculate the capital gains you can run:\n```bash\n$ capgains calc sample.csv 2017\nGOOG-2017\n[Total Gains = -1,028.54]\n+------------+--------------------+----------+----------+-------+---------+--------------+------------+-----------------+------------+----------------+-------------+----------+\n| date       | transaction_type   | ticker   | action   |   qty |   price |   commission |   currency |   share_balance |   proceeds |   capital_gain |   acb_delta |      acb |\n|------------+--------------------+----------+----------+-------+---------+--------------+------------+-----------------+------------+----------------+-------------+----------|\n| 2017-05-20 | RSU VEST           | GOOG     | SELL     |    50 |   45.00 |         0.00 |        CAD |              50 |   2,250.00 |      -1,028.54 |   -3,278.54 | 3,278.54 |\n+------------+--------------------+----------+----------+-------+---------+--------------+------------+-----------------+------------+----------------+-------------+----------+\n```\nYour CSV file can contain transactions spanning across multiple different tickers. You can filter the above commands by running the following:\n```bash\n$ capgains calc sample.csv 2017 -t GOOG\n...\n\n$ capgains show sample.csv -t GOOG\n...\n```\nFor additional commands and options, run one of the following:\n```bash\n$ capgains --help\n\n$ capgains <command> --help\n```\n',
    'author': 'Eddy Maric',
    'author_email': None,
    'maintainer': 'Eddy Maric',
    'maintainer_email': None,
    'url': 'https://github.com/EmilMaric/cad-capital-gains',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
