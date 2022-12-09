#
#   Timer singleton to measure function call length. Implements a total measured time dictionary.
#

import time

class _TimerSingleton:
    def __init__(self):
        self.TOTAL_MEASURE = dict()

    def measure(self, func):
        """
        Decorator for measuring function's running time.
        Includes time of inner function calls, hence not suitable for recursion.
        """
        def _measure(*args, **kw):
            fname = func.__qualname__
            if fname not in self.TOTAL_MEASURE:
                self.TOTAL_MEASURE[fname] = {'Wall Time': 0, 'CPU Time': 0, 'Runs': 0}
            start_wall_time = time.time()
            start_cpu_time = time.process_time()
            result = func(*args, **kw)
            self.TOTAL_MEASURE[fname]['Wall Time'] += time.time() - start_wall_time
            self.TOTAL_MEASURE[fname]['CPU Time'] += time.process_time() - start_cpu_time
            self.TOTAL_MEASURE[fname]['Runs'] += 1
            return result

        return _measure
        
    def report(self):
        return self.TOTAL_MEASURE;
        
Timer = _TimerSingleton()