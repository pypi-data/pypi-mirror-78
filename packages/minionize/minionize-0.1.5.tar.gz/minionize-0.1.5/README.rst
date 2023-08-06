
Rationale
---------

- You wrote a program ``a.out`` with some parameters
- You need to explore the space of parameters

Minionize is a solution to spawn a legion of ``a.out`` in a massively
parallel manner.
By minionizing your program, its inputs can be taken from various sources
(e.g filesystem, pub/sub). Also inputs can be acked or redelivered
to another minions.

.. note::

    .. code-block:: bash

        # simplest way of invoking minionize
        $) minionize a.out


How does it work
----------------

A classical pattern to do the above is to apply the master/worker pattern
where a master gives tasks to workers. Workers repeatedly fetch a new task
from a queue , run it and report back somewhere its status.

Minionize encapsulates ``a.out`` so that it can takes its inputs from a queue.

Currently we support:

- ``execo`` based queue: the queue is stored in a shared file system in your cluster (actually, there's no master)
- ``Google pub/sub`` based queue: the queue is hosted by Google

Some examples
-------------

- Simplest use: In this case the received params are appended to the
  minionized program. If you need more control on the params see below.

  - with `Execo` engine:

    .. code-block:: bash

        # Create the queue of params
        # You'll have to run this prior to launching your minions (adapt to
        # your need / make a regular script)
        $) python -c "from execo_engine.sweep import ParamSweeper; ParamSweeper('sweeps', sweeps=range(10), save_sweeps=True)"

        # start your minions
        $) MINION_ENGINE=execo minionize echo hello
        hello 0
        hello 1
        hello 2
        hello 3
        hello 4
        hello 5
        hello 6
        hello 7
        hello 8
        hello 9

    .. note::

        In other words the ``minionize`` wrapper lets you populate the queue
        with strings representing the parameter of your command line
- On a OAR cluster (Igrida/Grid5000):

  - Generate the queue for example with Execo

    .. code-block:: bash

        python -c "from execo_engine.sweep import ParamSweeper; ParamSweeper('sweeps', sweeps=range(1000), save_sweeps=True)"

    - Create your oar scan script:

    .. code-block:: bash

        #!/usr/bin/env bash

        #OAR -n kpd
        #OAR -l nodes=1,walltime=1:0:0
        #OAR -t besteffort
        #OAR -t idempotent

        # oarsub --array 10 -S ./oar.sh

        set -eux

        pip install minionize

        minionize echo "hello from $OAR_JOB_ID"

    - Start your minions

    .. code-block:: bash

        echo "MINION_ENGINE=execo" > .env
        oarsub --array 10 -S ./oar.sh

    .. note::

        ``.env`` file is read when minionizing so the scan script can
        remain the same whatever engine is used.

    - Example of output:

    .. code-block:: bash

        $) cat OAR.1287856.stdout
        [...]
        hello from 1287856 135
        hello from 1287856 139
        hello from 1287856 143
        hello from 1287856 147
        hello from 1287856 151
        hello from 1287856 155
        hello from 1287856 159
        hello from 1287856 163
        hello from 1287856 167
        [...]

    .. note::

        As expected params have been distributed to different minions

-  Custom parameters handling:
    The params sent to you program can be anything (e.g a python dict). In
    some cases (many actually), you'll need to transform these params to
    something that you program can understand. So you'll need to minionize
    your program by writing a custom Callback.

    ``examples/process.py``: gives you a glimpse on writing custom callbacks.

    - use it with `Execo` engine:


    .. code-block:: bash

        # generate the queue of task
        python -c "from execo_engine.sweep import ParamSweeper, sweep; ParamSweeper('sweeps', sweeps=sweep({'a': [0, 1], 'b': ['x', 't"]}), save_sweeps=True)"

        # start your minions
        MINION_ENGINE=execo python process.py


    - use it with `GooglePubSub` engine:

    .. code-block:: bash

        # start your minions
        MINION_ENGINE=google \
        GOOGLE_PROJECT_ID=gleaming-store-288314  \
        GOOGLE_TOPIC_ID=TEST \
        GOOGLE_SUBSCRIPTION=tada \
        GOOGLE_APPLICATION_CREDENTIALS=``/.gcp/gleaming-store-288314-2444b0d20a52.json \
        python process.py

Roadmap
-------

- Easy integration as docker entrypoint
- Support new queues (Redis stream, RabbitMQ, Kakfa ...)
- Support new abstractions to run container based application (docker, singularity...)
- Automatic encapsulation using a .minionize.yml
- minions statistics
- Keep in touch (matthieu dot simonin at inria dot fr)