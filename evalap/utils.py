import base64
import concurrent.futures
import functools
import importlib
import inspect
import io
import pkgutil
import re
import subprocess
import time
from itertools import product
from typing import Any

import pyarrow.parquet as pq
import requests
from jinja2 import BaseLoader, Environment
from PIL import Image
from requests import Response

#
# String utils
#


def render_jinja(template: str, **kwargs):
    env = Environment(loader=BaseLoader())
    t = env.from_string(template)
    return t.render(**kwargs)


def extract_code(text: str):
    """Return the last code block found"""
    # Find all blocks of code wrapped in triple backticks
    matches = re.findall(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    if matches:
        # Return the last code block found
        code = matches[-1]
        # Remove any leading or trailing whitespace
        code = code.strip()
        return code

    return text.strip()


def image_to_base64(image: Image.Image | dict, format: str | None = None):
    """
    Convert a PIL image to a base64-encoded PNG bytes string.
    """
    if isinstance(image, dict):
        pil_image = Image.open(io.BytesIO(image["bytes"]))
    else:
        pil_image = image

    format = format or pil_image.format
    with io.BytesIO() as buffer:
        pil_image.save(buffer, format=format)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def pandoc(content, input_format="html", output_format="markdown"):
    """
    Convert HTML to Markdown using Pandoc

    Parameters:
    - html_content: The HTML string to convert
    - output_format: The specific Markdown flavor (e.g., "markdown", "markdown_strict", "gfm" for GitHub-flavored Markdown)

    Returns:
    - Markdown text
    """
    # Create a process that runs pandoc
    process = subprocess.Popen(
        ["pandoc", "-f", input_format, "-t", output_format],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Send the HTML content to pandoc and get the output
    new_content, error = process.communicate(input=content)
    if process.returncode != 0:
        raise Exception(f"Pandoc conversion failed: {error}")

    return new_content


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
# API/HTTP utils
#


# Eventually cache with https://github.com/tkem/cachetools
# @cached(TTLCache(maxsize=256, ttl=86400))
def is_valid_url(url: str, timeout: int = 3) -> bool:
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except Exception:
        return False


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


def func_inspect(func, ignore:list[str]):
    func_info = {}
    # Inspect func method to extract parameters
    try:
        sig = inspect.signature(func)
        # Extract parameters with default values (excluding **kwargs)
        params_with_defaults = []
        params_without_defaults = []
        for param_name, param in sig.parameters.items():
            # Skip 'self' parameter
            if param_name in [
                "self",
                "model",
                "evaluation_model",
                "strict_mode",
                "async_mode",
                "verbose_mode",
            ]:
                continue

            # Skip if it's VAR_KEYWORD (**kwargs) or VAR_POSITIONAL (*args)
            if param.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
                continue

            # Check if parameter has a default value
            if param.default != inspect.Parameter.empty:
                params_with_defaults.append(param_name)
            else:
                params_without_defaults.append(param_name)

        func_info["required_params"] = params_without_defaults
        func_info["optional_params"] = params_with_defaults

    except (ValueError, TypeError) as e:
        # Handle cases where __init__ cannot be inspected
        print(f"Warning: Could not inspect func for {str(func)}: {e}")
        func_info["required_params"] = []
        func_info["optional_params"] = []

    return func_info

def import_classes(package_name: str, class_names: list[str], extra: list[str] = None) -> list[dict]:
    """Get a list of class obj from given package name and class_names.
    If `extra` is given, it tries to extract the object with that names in the same module where a class is found.

    Additionally extracts required and optional parameters from the class __init__ method.
    """
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
            class_info = {"name": class_name, "obj": cls, "extra": {}}

            # Add extra attributes from the module
            for x in extra or []:
                class_info["extra"][x] = getattr(module, x, None)

            func_info = func_inspect(
                cls.__init__,
                ignore=[
                    "self",
                    "model",
                    "evaluation_model",
                    "strict_mode",
                    "async_mode",
                    "verbose_mode",
                ],
            )
            class_info["required_params"] = func_info["required_params"]
            class_info["optional_params"] = func_info["optional_params"]

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
# Parquet utils
#


def get_parquet_row_by_index(parquet_file_path: str, row_index: int, batch_size: int = 10) -> dict:
    """
    Extract the ith row from a Parquet file using iter_batches

    Args:
        parquet_file_path: Path to the Parquet file
        row_index: The index of the row to extract (0-based)

    Returns:
        Dictionary representing the row data
    """
    # Open the parquet file
    pf = pq.ParquetFile(parquet_file_path)

    # Validate row index against total rows
    if row_index < 0 or row_index >= pf.metadata.num_rows:
        raise IndexError(f"Row index {row_index} out of bounds (total rows: {pf.metadata.num_rows})")

    # Iterate through batches until we find the one containing our row
    row = None
    current_row = 0
    for batch in pf.iter_batches(batch_size=batch_size):
        batch_size = len(batch)

        # Check if the target row is in this batch
        if current_row <= row_index < current_row + batch_size:
            # Calculate the local index within this batch
            local_index = row_index - current_row

            # Extract the row as a dictionary
            columns = pf.schema_arrow.names
            row = {col: batch[col][local_index].as_py() for col in columns}
            break

        # Move to the next batch
        current_row += batch_size

    return row


#
# Async utils
#


def run_with_timeout(func, timeout, *args, **kwargs):
    """Set a timeout in seconds before stopping execution."""
    # @DEBUG: generates OSError: [Errno 24] Too many open files
    #         + uncatchable exception
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            result = future.result(timeout=timeout)
            return result
        except concurrent.futures.TimeoutError:
            print("Function execution exceeded the timeout.")
            return None


#
# Misc
#


def build_param_grid(common_params: dict[str, Any], grid_params: dict[str, list[Any]]) -> list[dict[str, Any]]:
    """
    # Example usage:
    common_params = {
        "batch_size": 32,
        "model_params": {
            "dropout": 0.5,
            "activation": "relu"
        }
    }

    grid_params = {
        "learning_rate": [0.001, 0.01],
        "model_params": [
            {"hidden_layers": 2},
            {"hidden_layers": 3}
        ]
    }

    result = build_param_grid(common_params, grid_params)

    # Example of one entry in the result:
    # {
    #     "batch_size": 32,
    #     "learning_rate": 0.001,
    #     "model_params": {
    #         "dropout": 0.5,
    #         "activation": "relu",
    #         "hidden_layers": 2
    #     }
    # }
    """
    # Get all possible combinations of grid parameters
    keys = grid_params.keys()
    values = grid_params.values()
    combinations = list(product(*values))

    param_grid = []

    for combo in combinations:
        # Create a new dictionary starting with common_params
        params = common_params.copy()

        # Create dictionary for current combination
        current_combo = dict(zip(keys, combo))

        # For each parameter in the current combination
        for key, value in current_combo.items():
            if key in params and isinstance(params[key], dict) and isinstance(value, dict):
                # If both are dicts, merge at first level only
                params[key] = {**params[key], **value}
            else:
                # Otherwise, simply update the value
                params[key] = value

        param_grid.append(params)

    return param_grid
