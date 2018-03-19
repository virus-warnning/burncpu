import time
import queue
import random
import signal
import threading as th
import multiprocessing as mp

##
#
class WorkerDispatcher:

  # Sleep time after reading an empty process queue.
  # If this time was set 0, child process would be zombie after working for a while.
  IDLE_FOR_EMPTY_PQ = 0.5

  # Sleep time after reading an empty thread queue.
  # If this time was set 0, child process would always be busy even if no task in queue.
  IDLE_FOR_EMPTY_TQ = 1

  # Shared properties, don't modify them outside __init__()
  time_begin = 0
  time_limit = 0
  proc_count = 0
  worker_count = 0

  # Access in parent only.
  parent_prev_dispatch = 0
  parent_proc_list = []
  parent_queue_list = []
  parent_interrupted = False

  # Access in child only.
  child_pidx = 0
  child_interrupted = False

  def __init__(self, worker_count = 0, use_core = 0, time_limit = 0):
    self.time_begin = time.time()
    self.time_limit = time_limit
    self.parent_prev_dispatch = self.time_begin

    if use_core <= 0:
      self.proc_count = mp.cpu_count()
    else:
      self.proc_count = min(mp.cpu_count(), max(1, use_core - 1))

    if worker_count <= 0:
      self.worker_count = self.proc_count * 2
    else:
      self.worker_count = max(self.proc_count, worker_count)

    # Handle system signals.
    for s in [signal.SIGINT, signal.SIGTERM]:
      signal.signal(s, self.__parent_inthook)

    # Create processes by core count.
    for i in range(self.proc_count):
      queue = mp.Queue()
      queue.cancel_join_thread()
      proc = mp.Process(target=self.__process_worker, args=(i, queue))
      proc.start()
      self.parent_proc_list.append(proc)
      self.parent_queue_list.append(queue)

  def __elapsed(self):
    return time.time() - self.time_begin

  def __is_child_alive(self):
    # Terminated by time limit.
    if self.time_limit > 0:
      if self.__elapsed() > self.time_limit:
        return False

    # Terminated by system signal.
    if self.child_interrupted:
      return False

    return True

  def __process_worker(self, pidx, pqueue):
    # Initialize for child process
    self.child_pidx = pidx
    for s in [signal.SIGINT, signal.SIGTERM]:
      signal.signal(s, self.__child_inthook)

    # Create threads
    threads = []
    tqueues = []
    tidx = pidx
    while tidx < self.worker_count:
      tqueue = queue.Queue()
      thread = th.Thread(target=self.__thread_worker, args=(pidx, tidx, tqueue))
      thread.start()
      threads.append(thread)
      tqueues.append(tqueue)
      tidx = tidx + self.proc_count

    # Dispatch task to thread queue.
    while self.__is_child_alive():
      try:
        (tidx, func, args) = pqueue.get(False)
        if tidx is -1:
          n = random.randint(0, len(threads) - 1)
        else:
          n = int(tidx / self.proc_count)
        tqueue = tqueues[n]
        tqueue.put((func, *args))
      except queue.Empty:
        time.sleep(self.IDLE_FOR_EMPTY_PQ)

    # Wait for all thread
    for thread in threads:
      thread.join()

  def __thread_worker(self, pidx, tidx, tqueue):
    while self.__is_child_alive():
      try:
        (func, args) = tqueue.get(False)
        try:
          func.__call__(*args)
        except:
          pass
      except queue.Empty:
        time.sleep(self.IDLE_FOR_EMPTY_TQ)

  def __parent_inthook(self, sig, frame):
    print('Ctrl+C detected. (parent)')
    self.parent_interrupted = True

  def __child_inthook(self, sig, frame):
    print('Ctrl+C detected. (child #{})'.format(self.child_pidx))
    self.child_interrupted = True

  def dispatch(self, func, *args):
    idx   = random.randint(0, len(self.parent_proc_list) - 1)
    queue = self.parent_queue_list[idx]
    queue.put((-1, func, args))

  # Join all processes
  def join(self):
    # Wait for all processes.
    for p in self.parent_proc_list:
      p.join()

  def is_alive(self):
    if self.time_limit > 0:
      if self.__elapsed() > self.time_limit:
        return False

    if self.parent_interrupted:
      return False

    return True

def one_second_task(a, b):
  begin = time.time()
  while (time.time() - begin) < 1.0:
    a + b

def burn_your_cpu():
  BEGIN = time.time()

  # Create a worker dispatcher.
  # You can terminate workers by pressing Ctrl+C or waiting 60 seconds.
  wd = WorkerDispatcher(time_limit = 60)

  # Take a break.
  # There are "cores + 1" processes which are idle.
  time.sleep(10)

  # Let's go!
  # All of the child processes will be busy.
  for n in range(60 * mp.cpu_count()):
    wd.dispatch(one_second_task, (1, 0))

  wd.join()

  ELAPSED = time.time() - BEGIN
  print('Done ({:.2f}s)'.format(ELAPSED))

if __name__ == '__main__':
  burn_your_cpu()
