import functools
import time

from jinja2 import BaseLoader, Environment
from requests import Response

#
# String utils
#


def render_jinja(template: str, **kwargs):
    env = Environment(loader=BaseLoader())
    t = env.from_string(template)
    return t.render(**kwargs)


#
# API utils
#


def retry(tries: int = 3, delay: int = 2):
    """
    A simple retry decorator that catch exception to retry multiple times
    @TODO: only catch only network error/timeout error.

    Parameters:
    - tries: Number of total attempts.
    - delay: Delay between retries in seconds.
    """

    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = tries
            while attempts > 1:
                try:
                    return func(*args, **kwargs)
                # @TODO: Catch network error.
                # except (requests.exceptions.RequestException, httpx.RequestError) as e:
                except Exception as e:
                    print(f"Error: {e}, retrying in {delay} seconds...")
                    time.sleep(delay)
                    attempts -= 1
            # Final attempt without catching exceptions
            return func(*args, **kwargs)

        return wrapper

    return decorator_retry


def log_and_raise_for_status(response: Response, msg_on_error: str = "API Error detail"):
    # response from requests module
    if not response.ok:
        try:
            error_detail = response.json().get("detail")
        except Exception:
            error_detail = response.text
        print(f"{msg_on_error}: {error_detail}\n")
        response.raise_for_status()
