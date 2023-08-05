import time


def retry_on_exception(exceptions, max_retries=1, sleep_secs=0.0):
    assert tuple(exceptions)
    assert max_retries >= 1
    
    def decorate(func):
        def decorator(*args, **kwargs):
            retries_count = -1
            
            while True:
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as exception:
                    retries_count += 1
                    
                    if retries_count == max_retries:
                        raise
                
                time.sleep(sleep_secs)
        
        return decorator
    
    return decorate
