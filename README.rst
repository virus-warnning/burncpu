Module burncpu is a worker dispatcher with multiprocessing and multithreading.

Features
========
- All CPU cores can be used.
- Workers can be stopped gracefully by system signals.
- Easy to use.

WorkerDispatcher Reference
==========================


Sample
======
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
