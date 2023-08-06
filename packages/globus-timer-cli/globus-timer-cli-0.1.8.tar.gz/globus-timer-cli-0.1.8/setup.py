# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timer_cli']

package_data = \
{'': ['*']}

install_requires = \
['fair-research-login>=0.1.5,<0.2.0',
 'requests>=2.24.0,<3.0.0',
 'typer>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['globus-timer = timer_cli.main:main']}

setup_kwargs = {
    'name': 'globus-timer-cli',
    'version': '0.1.8',
    'description': 'CLI for interacting with the timer API',
    'long_description': '# Globus Automate Timer CLI\n\nThis is an alpha-version CLI for use with the (also in alpha) timer API, to use\nprimarily for scheduling recurring transfer tasks through Globus Automate.\n\n## What is this Service/CLI for?\n\nThe timer service can be used to schedule recurring transfer tasks. For example,\nlet’s say we want to have a transfer automatically run every night to back up\ndata. We submit a job to the timer API starting tonight, and with an interval of\n1 day at which it will be re-run. In that request we provide the timer service\nthe same input we would give to the transfer action provider; that part of the\nrequest contains the information for what endpoints we transfer to and from as\nwell as other options relevant to the transfer.\n\n## Installation\n\nThis CLI requires Python version 3.5 or higher. See the [Globus CLI\ndocs](https://docs.globus.org/cli/installation/prereqs/) for help on how to set\nup Python.\n\nOnce the appropriate version of Python is ready, install with `pip install\nglobus-timer-cli`.\n\n## Transfer Quickstart\n\n```\nglobus-timer job transfer \\\n    --name example-job\n    --interval 28800\n    --start \'2020-01-01T12:34:56\'\n    --source-endpoint ddb59aef-6d04-11e5-ba46-22000b92c6ec \\\n    --dest-endpoint ddb59af0-6d04-11e5-ba46-22000b92c6ec \\\n    --item ~/file1.txt ~/new_file1.txt false\n    --item ~/file2.txt ~/new_file2.txt false\n```\nSpecify any number of `--item`, which will be transferred from the source\nendpoint to the destination endpoint at the interval specified, beginning at the\nstart time. The start time is inferred to be in the local timezone if an offset\nis not specified. See `globus-timer job transfer --help` for additional details.\n\nThe results should contain a UUID in the field `job_id` which tracks this job in\nthe timer service. To check on the results of your transfers, use:\n```\nglobus-timer job status JOB_ID\n```\n\n## Basic Usage\n\nWhile part of the CLI is tailored to submitting transfer tasks, the interface\nprovides for scheduling generic actions in the Globus Automate API. To\nsummarize, the CLI can be used for the following tasks:\n- Schedule a new recurring job: `globus-timer job submit ...`\n- Check the list of previously-submitted jobs: `globus-timer job list`\n- Check on the status of a particular job: `globus-timer job status JOB_ID`\n- Show help for any of the above commands with `globus-timer job submit --help`\n  etc.\n\nAs an example, a complete command would look something like this:\n\n```\nglobus-timer job submit \\\n    --name test-tutorial-job \\\n    --interval 600 \\\n    --action-url https://actions.automate.globus.org/transfer/transfer/run \\\n    --action-body \'{"body": {"source_endpoint_id": "ddb59aef-6d04-11e5-ba46-22000b92c6ec", "destination_endpoint_id": "ddb59af0-6d04-11e5-ba46-22000b92c6ec", "transfer_items": [{"source_path": "/~/file1.txt", "destination_path": "/~/new_file1.txt"}]}}\'\n```\n\nEach command should be reasonably informative as to what arguments are required,\nand what type of input is expected for those arguments. However, do note that\nthe `action-body` depends on the schema expected for that action provider, which\nisn\'t known by the CLI. You can use the [Globus Automate\nclient](https://pypi.org/project/globus-automate-client/) to introspect the\ninput schema for an action provider, which is what the CLI needs for the\n`--action-body` parameter. As for the other options, a quick breakdown:\n\n- `--name` is just for the user to track their own submissions, and does not\n  need to be unique\n- `--interval`, for the job to re-run at, is in units of seconds\n- `--start` is optional, defaulting to the current time, and allowed formats are\n  listed in `globus-timer job submit --help`\n- Instead of `--action-body` you can also give `--action-file` which should be a\n  relative filepath to a file containing the same action body as JSON\n\nTo schedule transfers on your behalf, this CLI requires authentication through\nGlobus Auth. The CLI should initially prompt you with a Globus Auth page to\nconsent to this usage. Authentication information is cached in the file\n`~/.config/globus/tokens.json` (so the authentication process is only needed on\nthe first use), which should be kept secret.\n\n## How Does it Work?\n\nInternally, the service is using an algorithm similar to the unix utility cron.\nThe service will operate under the following guarantees:\n- A job will not run more frequently than the specified interval.\n- The time that a job starts may skew slightly depending on load (likely on the\n  order of fractions of a second to individual seconds), but does not skew\n  further over time. For example, suppose that your job is meant to run every 10\n  seconds, but the scheduler is under unusually heavy load each time, and your\n  job runs 1 second later than scheduled. It would not be possible for the job\n  to run at 11, 22, 33, … rather it runs at 11, 21, 31, …\n- Jobs are "soft-deleted," meaning they are removed from the scheduler but not\n  the database, so the outputs of previous runs are still available. The results\n  of the previous 10 runs are exposed in the API wherever the job is returned.\n\n',
    'author': 'Rudyard Richter',
    'author_email': 'rudyard@globus.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
