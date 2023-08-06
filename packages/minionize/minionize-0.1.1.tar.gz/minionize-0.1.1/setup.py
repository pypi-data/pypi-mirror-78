# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minionize']

package_data = \
{'': ['*']}

install_requires = \
['execo>=2.6.4,<3.0.0', 'google-cloud-pubsub>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['minionize = minionize.cli:run']}

setup_kwargs = {
    'name': 'minionize',
    'version': '0.1.1',
    'description': 'Massively Parallel operation made easy',
    'long_description': '\nRationale\n---------\n\n- You wrote a program ``a.out`` with some parameters\n- You need to explore the space of parameters\n\nMinionize is a solution to spawn a legion of ``a.out`` in a massively\nparallel manner.\n\n.. note::\n\n    .. code-block:: bash\n\n        $) minionize a.out\n\n    will wait for inputs coming from a source and invoke ``a.out`` upon\n    reception. Depending on the command outcome, the inputs may be acked or\n    redelivered to another minion.\n\nHow does it work\n----------------\n\nA classical pattern to do the above is to apply the master/worker pattern\nwhere a master give tasks to workers. Workers repeatedly fetch a new task\nfrom a queue , run it and report back somewhere its status.\n\nMinionize encapsulates ``a.out`` so that it can takes its inputs from a queue.\n\nCurrently we support:\n\n- ``execo`` based queue: the queue is stored in a shared file system in your cluster\n- ``Google pub/sub`` based queue: the queue is hosted by Google.\n\nSome examples\n-------------\n\n- ``examples/process.py``: run your program as a subprocess each time a new parameter comes.\n    - use it with `Execo` engine:\n\n\n    .. code-block:: bash\n\n        # generate the queue of task\n        python -c "from execo_engine.sweep import ParamSweeper, sweep; ParamSweeper(\'sweeps\', sweeps=sweep({\'a\': [0, 1], \'b\': [\'x\', \'t"]}), save_sweeps=True)"\n\n        # start your minions\n        EP=execo python process.py\n\n\n    - use it with `GooglePubSub` engine:\n\n    .. code-block:: bash\n\n        # start your minions\n        EP=google \\\n        GOOGLE_PROJECT_ID=gleaming-store-288314  \\\n        GOOGLE_TOPIC_ID=TEST \\\n        GOOGLE_SUBSCRIPTION=tada \\\n        GOOGLE_APPLICATION_CREDENTIALS=``/.gcp/gleaming-store-288314-2444b0d20a52.json \\\n        python process.py\n\nRoadmap\n-------\n\n- Easy integration as docker entrypoint\n- Support new queues (Redis stream, RabbitMQ, Kakfa ...)\n- Support new abstractions to run container based application (docker, singularity...)\n- Automatic encapsulation using a .minionize.yml\n- Keep in touch (matthieu dot simonin at inria dot fr)',
    'author': 'msimonin',
    'author_email': 'matthieu.simonin@inria.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.inria.fr/msimonin/minionize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
