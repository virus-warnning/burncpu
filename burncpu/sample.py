import time
import multiprocessing as mp
from burncpu.dispatcher import WorkerDispatcher

def one_second_task(a, b):
  begin = time.time()
  while (time.time() - begin) < 1.0:
    a + b

def burn_cpu():
  BEGIN = time.time()

  # Create a worker dispatcher.
  # You can terminate workers by pressing Ctrl+C or waiting 60 seconds.
  wd = WorkerDispatcher(time_limit = 60)

  # Take a break.
  # There are "cores + 1" processes which are idle.
  wd.sleep(10)

  # Let's go!
  # All of the child processes will be busy.
  for n in range(60 * mp.cpu_count()):
    wd.dispatch(one_second_task, (1, 0))

  wd.join()

  ELAPSED = time.time() - BEGIN
  print('Done ({:.2f}s)'.format(ELAPSED))

if __name__ == '__main__':
  burn_cpu()
