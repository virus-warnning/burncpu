Module burncpu is a worker dispatcher with multiprocessing and multithreading.

Features
========
- All CPU cores can be used.
- Workers can be stopped gracefully by system signals.
- Easy to use.

Quickstart
==========
Use the following command to run the sample module.

.. code:: bash

  python3 -m burncpu.sample

Then monitor CPU status, some changes take place at these time.

====  =================================================
Time                        Events
====  =================================================
  0s   All CPU cores are IDLE.
 10s   Workers begin to call one_second_task many times.
 60s   Workers begin to terminate.
====  =================================================

Pressing Ctrl+C or sending system signal can also terminate the sample.

Finally copy and modify the `source code <https://github.com/virus-warnning/burncpu/blob/master/burncpu/sample.py>`_ to make your own.

Reference
=========

.. code:: python

  from burncpu.dispatcher import WorkerDispatcher

WorkerDispatcher.__init__(worker_count=0, use_core=0, time_limit=0)
Create a dispatcher instace.
:worker_count: How many threads would be created, 0 means create ([use_core] * 2) threads.
:use_core: How many cores would be use, 0 means all cores.
:time_limit: Stop workers after [time_limit] seconds.

WorkerDispatcher.dispatch(func, *args)
Dispatch a function to be called by worker.
:func: Function to be called by worker.
:args: Argument list of this function.

WorkerDispatcher.sleep(seconds)
Sleep dispatcher.
:seconds: Sleep time. Dispatcher would not sleep given seconds actually.
          It sleep many times during given seconds, so that system signal can be handled.

WorkerDispatcher.join()
Wait for running functions.

WorkerDispatcher.is_alive()
Check if the dispatcher is alive.
