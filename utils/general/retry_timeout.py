import time
from utils.general.load_env import app_settings

class RetryState:
    def __init__(self):
        self.callback = lambda: print("No func_at_fail")

retry_state = RetryState()

def retry(max_attempts=app_settings["retry_count"], delay=app_settings["retry_delay"], func_at_fail=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    # print(f'Calling {func.__name__} with {args} {kwargs}')
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Attempt {i+1} failed with error: {e}")
                    if func_at_fail:
                        func_at_fail()
                    time.sleep(delay)
            raise Exception(f"Function {func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator
