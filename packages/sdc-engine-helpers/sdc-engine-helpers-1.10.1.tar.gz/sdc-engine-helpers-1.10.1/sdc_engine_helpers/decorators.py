"""
   SDC engine helper decorators module
"""
import time
from functools import wraps


def retry_handler(
        exceptions,
        total_tries: int = 4,
        initial_wait: float = 0.5,
        backoff_factor: int = 2
):
    """
        Decorator - retry n times when there are exceptions

        args:
            exceptions: Exception instance or list of Exception instances to catch & retry
            total_tries (int): Total retry attempts
            initial_wait (float): initial delay between retry attempts in seconds
            backoff_factor (int): multiplier used to further randomize back off

        return:
            wrapped function's response
    """

    def retry_decorator(func):
        @wraps(func)
        def func_with_retries(*args, **kwargs):
            """
                Wrapper function to decorate function with retry functionality
            """
            tries, delay = 0, initial_wait
            while tries < total_tries:
                try:
                    print(f'Attempt {tries + 1}')
                    return func(*args, **kwargs)
                except exceptions as ex:
                    tries += 1

                    if tries == total_tries:
                        print(
                            'Function: {name}\n'
                            'Failed despite best efforts after {tries} tries'.format(
                                name=func.__name__,
                                tries=tries
                            )
                        )
                        raise ex

                    print(
                        'Function: {name}\n'
                        'Exception {exception}.\n'
                        'Retrying in {delay} seconds!'.format(
                            name=func.__name__,
                            exception=str(ex),
                            delay=delay
                        )
                    )

                    time.sleep(delay)

                    delay *= backoff_factor

        return func_with_retries

    return retry_decorator
