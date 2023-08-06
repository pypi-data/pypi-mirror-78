# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minionize', 'minionize.tests.unit']

package_data = \
{'': ['*']}

install_requires = \
['execo>=2.6.4,<3.0.0',
 'google-cloud-pubsub>=1.7.0,<2.0.0',
 'python-dotenv>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['minionize = minionize.cli:run']}

setup_kwargs = {
    'name': 'minionize',
    'version': '0.1.5',
    'description': 'Massively Parallel operations made easy',
    'long_description': '\nRationale\n---------\n\n- You wrote a program ``a.out`` with some parameters\n- You need to explore the space of parameters\n\nMinionize is a solution to spawn a legion of ``a.out`` in a massively\nparallel manner.\nBy minionizing your program, its inputs can be taken from various sources\n(e.g filesystem, pub/sub). Also inputs can be acked or redelivered\nto another minions.\n\n.. note::\n\n    .. code-block:: bash\n\n        # simplest way of invoking minionize\n        $) minionize a.out\n\n\nHow does it work\n----------------\n\nA classical pattern to do the above is to apply the master/worker pattern\nwhere a master gives tasks to workers. Workers repeatedly fetch a new task\nfrom a queue , run it and report back somewhere its status.\n\nMinionize encapsulates ``a.out`` so that it can takes its inputs from a queue.\n\nCurrently we support:\n\n- ``execo`` based queue: the queue is stored in a shared file system in your cluster (actually, there\'s no master)\n- ``Google pub/sub`` based queue: the queue is hosted by Google\n\nSome examples\n-------------\n\n- Simplest use: In this case the received params are appended to the\n  minionized program. If you need more control on the params see below.\n\n  - with `Execo` engine:\n\n    .. code-block:: bash\n\n        # Create the queue of params\n        # You\'ll have to run this prior to launching your minions (adapt to\n        # your need / make a regular script)\n        $) python -c "from execo_engine.sweep import ParamSweeper; ParamSweeper(\'sweeps\', sweeps=range(10), save_sweeps=True)"\n\n        # start your minions\n        $) MINION_ENGINE=execo minionize echo hello\n        hello 0\n        hello 1\n        hello 2\n        hello 3\n        hello 4\n        hello 5\n        hello 6\n        hello 7\n        hello 8\n        hello 9\n\n    .. note::\n\n        In other words the ``minionize`` wrapper lets you populate the queue\n        with strings representing the parameter of your command line\n- On a OAR cluster (Igrida/Grid5000):\n\n  - Generate the queue for example with Execo\n\n    .. code-block:: bash\n\n        python -c "from execo_engine.sweep import ParamSweeper; ParamSweeper(\'sweeps\', sweeps=range(1000), save_sweeps=True)"\n\n    - Create your oar scan script:\n\n    .. code-block:: bash\n\n        #!/usr/bin/env bash\n\n        #OAR -n kpd\n        #OAR -l nodes=1,walltime=1:0:0\n        #OAR -t besteffort\n        #OAR -t idempotent\n\n        # oarsub --array 10 -S ./oar.sh\n\n        set -eux\n\n        pip install minionize\n\n        minionize echo "hello from $OAR_JOB_ID"\n\n    - Start your minions\n\n    .. code-block:: bash\n\n        echo "MINION_ENGINE=execo" > .env\n        oarsub --array 10 -S ./oar.sh\n\n    .. note::\n\n        ``.env`` file is read when minionizing so the scan script can\n        remain the same whatever engine is used.\n\n    - Example of output:\n\n    .. code-block:: bash\n\n        $) cat OAR.1287856.stdout\n        [...]\n        hello from 1287856 135\n        hello from 1287856 139\n        hello from 1287856 143\n        hello from 1287856 147\n        hello from 1287856 151\n        hello from 1287856 155\n        hello from 1287856 159\n        hello from 1287856 163\n        hello from 1287856 167\n        [...]\n\n    .. note::\n\n        As expected params have been distributed to different minions\n\n-  Custom parameters handling:\n    The params sent to you program can be anything (e.g a python dict). In\n    some cases (many actually), you\'ll need to transform these params to\n    something that you program can understand. So you\'ll need to minionize\n    your program by writing a custom Callback.\n\n    ``examples/process.py``: gives you a glimpse on writing custom callbacks.\n\n    - use it with `Execo` engine:\n\n\n    .. code-block:: bash\n\n        # generate the queue of task\n        python -c "from execo_engine.sweep import ParamSweeper, sweep; ParamSweeper(\'sweeps\', sweeps=sweep({\'a\': [0, 1], \'b\': [\'x\', \'t"]}), save_sweeps=True)"\n\n        # start your minions\n        MINION_ENGINE=execo python process.py\n\n\n    - use it with `GooglePubSub` engine:\n\n    .. code-block:: bash\n\n        # start your minions\n        MINION_ENGINE=google \\\n        GOOGLE_PROJECT_ID=gleaming-store-288314  \\\n        GOOGLE_TOPIC_ID=TEST \\\n        GOOGLE_SUBSCRIPTION=tada \\\n        GOOGLE_APPLICATION_CREDENTIALS=``/.gcp/gleaming-store-288314-2444b0d20a52.json \\\n        python process.py\n\nRoadmap\n-------\n\n- Easy integration as docker entrypoint\n- Support new queues (Redis stream, RabbitMQ, Kakfa ...)\n- Support new abstractions to run container based application (docker, singularity...)\n- Automatic encapsulation using a .minionize.yml\n- minions statistics\n- Keep in touch (matthieu dot simonin at inria dot fr)',
    'author': 'msimonin',
    'author_email': 'matthieu.simonin@inria.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.inria.fr/msimonin/minionize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
