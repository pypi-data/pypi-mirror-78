
Rationale
---------

- You wrote a program ``a.out`` with some parameters
- You need to explore the space of parameters

Minionize is a solution to spawn a legion of ``a.out`` in a massively
parallel manner.

.. note::

    .. code-block:: bash

        $) minionize a.out

    will wait for inputs coming from a source and invoke ``a.out`` upon
    reception. Depending on the command outcome, the inputs may be acked or
    redelivered to another minion.

How does it work
----------------

A classical pattern to do the above is to apply the master/worker pattern
where a master give tasks to workers. Workers repeatedly fetch a new task
from a queue , run it and report back somewhere its status.

Minionize encapsulates ``a.out`` so that it can takes its inputs from a queue.

Currently we support:

- ``execo`` based queue: the queue is stored in a shared file system in your cluster
- ``Google pub/sub`` based queue: the queue is hosted by Google.

Some examples
-------------

- ``examples/process.py``: run your program as a subprocess each time a new parameter comes.
    - use it with `Execo` engine:


    .. code-block:: bash

        # generate the queue of task
        python -c "from execo_engine.sweep import ParamSweeper, sweep; ParamSweeper('sweeps', sweeps=sweep({'a': [0, 1], 'b': ['x', 't"]}), save_sweeps=True)"

        # start your minions
        EP=execo python process.py


    - use it with `GooglePubSub` engine:

    .. code-block:: bash

        # start your minions
        EP=google \
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
- Keep in touch (matthieu dot simonin at inria dot fr)