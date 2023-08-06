import time
import functools
from functools import lru_cache

import sys


#https://realpython.com/pypi-publish-python-package/


#prints the returned value of a funtion
def print_result(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res=func(*args, **kwargs)
        print(res)
        return res
    return wrapper

#@print_result
#def add(num1,num2,num3):
#    return num1+num2+num3



#prints the execution time of a function
#takes unit as optional input
#usage @timeit,@timeit(unit="millisec"),@timeit(unit="sec"),@timeit(unit="min")
#default is sec

def timeit(func=None,unit='sec'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = func(*args, **kwargs)
            te = time.time()

            if (unit == "sec"):
                print('%r  %2.10f sec' % (func.__name__, (te - ts)))
            elif (unit == "millisec"):
                print('%r  %2.10f millisec' % (func.__name__, (te - ts) * 1000))
            elif (unit == "min"):
                print('%r  %2.10f min' % (func.__name__, (te - ts) / 60))

            return result
        return wrapper

    if func is not None:
        return decorator(func)
    return decorator

#@timeit(unit='millisec')
#def add(num1,num2,num3):
#    time.sleep(1)
#    return num1+num2+num3





# Prints the input parameters of the called function.
def print_input_params(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("args",args)
        print("kwargs",kwargs)
        return func(*args, **kwargs)

    return wrapper

#@print_input_params
#def add(num1,num2,num3):
#    return num1+num2+num3



class debug_context():
    """ Debug context to trace any function calls inside the context """

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print('Entering Debug Decorated func')
        # Set the trace function to the trace_calls function
        # So all events are now traced
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        pass
        # Stop tracing all events
        #sys.settrace = None

    def trace_calls(self, frame, event, arg):
        # We want to only trace our call to the decorated function
        if event != 'call':
            return
        elif frame.f_code.co_name != self.name:
            return
        # return the trace function to use when you go into that
        # function call
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # If you want to print local variables each line
        # keep the check for the event 'line'
        # If you want to print local variables only on return
        # check only for the 'return' event
        if event not in ['line', 'return']:
            return
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        local_vars = frame.f_locals
        print ('  {0} {1} {2} locals: {3}'.format(func_name,
                                                  event,
                                                  line_no,
                                                  local_vars))


# prints the values of variables line by line during its execution
#@debug_this
def debug_this(func):
    """ Debug decorator to call the function within the debug context """
    @functools.wraps(func)
    def decorated_func(*args, **kwargs):
        with debug_context(func.__name__):
            return_value = func(*args, **kwargs)
        return return_value
    return decorated_func

#@debug_this
#def add(num1,num2,num3):
#    res = num1+num2+num3
#    return res



#cache the result of the function
#size_limit default to 0(unlimited entires are stored)
#size_limit number of results to cache if exceeded the oldest cached results are removed first
#expiry_time default  to 0 (lasts till program is terminated)
#time in seconds that a entry that is cached should exist after this time perticular entry is cleared from cache

#quick_key_access, When set to true, a lookup table is stored for each key that is generated.
# This is set to false by default but if you're remembering a lot of values, then this may help get a speed boost at the cost of taking up more space.
# Simply, when set to false, this is slower but will take up less space, when set to true, this is faster but will take up more space


def cache(size_limit=0, expiry_time=0, quick_key_access=False):
    def decorator(func):
        storage = {}
        ttls = {}
        keys = []

        def wrapper(*args, **kwargs):
            # Generate a key based on arguments being passed
            key = (*args,) + tuple([(k, v) for k, v in kwargs.items()])

            # Check if they return value is already known
            if key in storage:
                result = storage[key]
            else:
                # If not, get the result
                result = func(*args, **kwargs)
                storage[key] = result

                # If a ttl has been set, remember when it is going to expire
                if expiry_time != 0:
                    ttls[key] = time.time() + expiry_time

                # If quick_key_access is being used, remember the key
                if quick_key_access:
                    keys.append(key)

                # If a size limit has been set, make sure the size hasn't been exceeded
                if size_limit != 0 and len(storage) > size_limit:
                    if quick_key_access:
                        oldest_key = keys[0]
                        del keys[0]
                    else:
                        oldest_key = list(storage.keys())[0]
                    del storage[oldest_key]

            # Check ttls if it is enabled
            if expiry_time != 0:
                while True:
                    if quick_key_access:
                        oldest_key = keys[0]
                    else:
                        oldest_key = list(storage.keys())[0]

                    # If they key has expired, remove the entry and it's quick access key if quick_key_access=True
                    if ttls[oldest_key] < time.time():
                        del storage[oldest_key]
                        if quick_key_access:
                            del keys[0]
                    else:
                        break

            return result
        return wrapper
    return decorator



#@cache(10, 60 * 5, True)
#def my_sum(a, b, c, d=1, e=5):
#    return a + b + c + d + e



# reties if error araises
#default is 3 times
def retry(func=None,tries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count=tries
            while(count>0):
                try:
                    return func(*args, **kwargs)
                except:
                    count-=1
        return wrapper

    if func is not None:
        return decorator(func)
    return decorator

#@retry(tries=4)
#def add(num1,num2,num3):
#    return num1+num2+num3




def wrap_try_except(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    return wrapper




#@wrap_try_except
#def divide(num1,num2):
#    return num1/num2

#divide(4,0)








