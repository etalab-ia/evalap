import concurrent.futures
import functools
import importlib
import pkgutil
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
# Time utils
#


class Timer:
    """Usage

    with Timer() as timer:
        some_function()

    print(f"The function took {timer.execution_time} seconds to execute.")
    """

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.execution_time = self.end_time - self.start_time


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


#
# Modules
#


def import_classes(package_name: str, class_names: list[str], more: list[str] = None) -> list[dict]:
    # Import the package
    package = importlib.import_module(package_name)

    # Iterate over all modules in the package
    classes = []
    remaining_classes = set(class_names)
    for finder, name, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        # Import the module
        try:
            module = importlib.import_module(name)
        except Exception as e:
            print(f"Failed to import module {name}: {e}")
            continue

        # Check for each class in the module
        found_classes = remaining_classes.intersection(dir(module))
        for class_name in found_classes:
            cls = getattr(module, class_name)
            class_info = {"name": class_name, "obj": cls}
            for extra in more or []:
                class_info[extra] = getattr(module, extra, None)
            classes.append(class_info)
            remaining_classes.remove(class_name)

        # Stop if all classes have been found
        if not remaining_classes:
            break

    if remaining_classes:
        raise ValueError(f"Warning: The following classes were not found: {remaining_classes}")

    # Reorder the list of class
    class_indexes = {name: index for index, name in enumerate(class_names)}
    classes = sorted(classes, key=lambda d: class_indexes[d["name"]])

    return classes


#
# Async utils
#


def run_with_timeout(func, timeout, *args, **kwargs):
    """Set a timeout in seconds before stopping execution."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            result = future.result(timeout=timeout)
            return result
        except concurrent.futures.TimeoutError:
            print("Function execution exceeded the timeout.")
            return None
