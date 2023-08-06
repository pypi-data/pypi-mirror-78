# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweet_delete']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.6.1,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'gevent>=20.6.2,<21.0.0',
 'numpy>=1.19.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-twitter>=3.5,<4.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'sparklines>=0.4.2,<0.5.0']

entry_points = \
{'console_scripts': ['tweet-delete = tweet_delete.entry:cli',
                     'vscode = vscode:vscode']}

setup_kwargs = {
    'name': 'tweet-delete',
    'version': '0.2.2',
    'description': 'Self-destructing Tweet tool',
    'long_description': '[![Build Status](https://travis-ci.org/brndnmtthws/tweet-delete.svg?branch=master)](https://travis-ci.org/brndnmtthws/tweet-delete) [![Maintainability](https://api.codeclimate.com/v1/badges/f50f5c31185dd44e5611/maintainability)](https://codeclimate.com/github/brndnmtthws/tweet-delete/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/f50f5c31185dd44e5611/test_coverage)](https://codeclimate.com/github/brndnmtthws/tweet-delete/test_coverage) [![PyPI version](https://badge.fury.io/py/tweet-delete.svg)](https://badge.fury.io/py/tweet-delete)\n\n# tweet-delete \U0001f99c🔫\n\n`tweet-delete` is a small Python tool for automatically deleting your tweets\nafter some specified amount of time. It is intended to be used to create\nself-destructing tweets. `tweet-delete` runs continuously, and will check\nyour timeline every hour to see if there are any new tweets which\nneed to be deleted. You may also specify a minimum engagement metric, which\nallows you to delete only the tweets that are junk 🗑.\n\nSelf-destructing tweets are the hippest, trendiest, coolest thing on\n[Twitter](https://twitter.com/) right now. Want to be cool and hip? You need\n`tweet-delete`. By creating artificial scarcity you can ten ex (10x) or\none-hundred ex (100x) your personal brand. 😎\n\nIn spite of the low technical barrier to entry for using this Twitter bot (or\nany similar ones), it does require following some instructions, and the\nTwitter dev account approval process is long and arduous. In other words, you\nwill easily be in the top 0.1% of technically skilled Twitter users. You will\nbe _super extra hip and cool_, and in the upper echelons of thought\nleadership, simply by using this tool. Wear your badge of honour loud and\nproud. Perhaps write "**These tweets self destruct.**" in your bio?\n\n## Quickstart\n\n_NOTE: This tool will delete your tweets. Please do not use this tool if you\ndon\'t want your tweets to be deleted._\n\n### 1. Set up Twitter Dev account\n\nTo get started, you\'ll need to go to\n[https://developer.twitter.com/en/apps](https://developer.twitter.com/en/apps)\nand set up a Twitter developer account, and create an "App".\n\nOnce you\'re approved (after several days or weeks of waiting), move on to the\nnext step.\n\n### 2. Generate API access tokens\n\n[Follow the instructions\nhere](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens)\nto generate your API access tokens. Save these somewhere, as you\'ll be\nneeding them later.\n\n### 3. Find a place to run the codes\n\nYou\'ll need a computer somehere, perhaps somewhere up in the clouds, to run\nthe codes. For your convenience, this repo includes a [Helm\nchart](https://helm.sh/) to run this tool on Kubernetes, which is extremely\nAI these days (if you hadn\'t heard).\n\n### 4. Install\n\nThis is a standard Python package, which can be installed using pip:\n\n```ShellSession\n$ pip install tweet-delete\n...\n```\n\nAlternatively, you can simply use the [pre-built Docker\nimage](https://hub.docker.com/r/brndnmtthws/tweet-delete) if you prefer.\n\n### 5. Run\n\nRun the script by passing it the API keys you generated above. It will run\ncontinuously, and tweet all tweets that are older than `--delete-older-than`\ndays starting on Jan 1, 2019.\n\n```ShellSession\n$ tweet-delete \\\n    --consumer_key=<consumer_key> \\\n    --consumer_secret=<consumer_secret> \\\n    --access_token_key=<access_token_key> \\\n    --access_token_secret=<access_token_secret> \\\n    --delete_older_than="7 days" \\\n    --delete_everything_after=2019-01-01 \\\n    --minimum_engagement=1\n...\n```\n\nNow the script will run forever, and delete all of your tweets older than 7\ndays as long as it\'s running. Congratulations! 🎉🎊\U0001f973\n\n## Performance\n\nThe script features an asynchronous, event-driven core, base on the excellent\n[gevent](http://www.gevent.org/) library. `tweet-delete` should have no\ndifficulty achieving a tweet deletes per second (TDPS) throughput well in\nexcess of 1,000 TDPS. However, practically speaking, you will likely hit the\nTwitter API rate limits long before hitting the script\'s limits.\n\n## Deployment with Helm\n\nThere\'s a [Helm](https://helm.sh/) chart included for your convenience. To use the chart, copy [helm/tweet-delete/values.yaml](helm/tweet-delete/values.yaml) somewhere, and install the chart:\n\nNow install the chart:\n\n```ShellSession\n$ cp helm/tweet-delete/values.yaml myvalues\n$ helm upgrade --install tweet-delete helm/tweet-delete -f myvalues.yaml\nRelease "tweet-delete" has been upgraded. Happy Helming!\nLAST DEPLOYED: Wed Mar 13 15:08:31 2019\nNAMESPACE: default\nSTATUS: DEPLOYED\n\nRESOURCES:\n==> v1/Deployment\nNAME          READY  UP-TO-DATE  AVAILABLE  AGE\ntweet-delete  0/1    1           0          46s\n\n==> v1/Pod(related)\nNAME                           READY  STATUS             RESTARTS  AGE\ntweet-delete-79bdbd995b-2mrmj  0/1    ContainerCreating  0         0s\n```\n\nSweeeeeet 😎\n\n## How can I recover deleted tweets?\n\nYou can\'t! They\'re gone!\n\nIf your account is public, it\'s possible that your tweets have been archived\nsomewhere. The internet is a semi-free and open place, so it\'s relatively\neasy to archive anything you find on it. For example, you may want to try\nrecovering your old tweets from\n[https://snapbird.org/](https://snapbird.org/).\n\n## Limitations\n\nTwitter does not let you retrieve more than 3,200 tweets from their public\nAPI, thus you cannot delete more than 3,200.\n',
    'author': 'Brenden Matthews',
    'author_email': 'brenden@brndn.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brndnmtthws/tweet-delete',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
