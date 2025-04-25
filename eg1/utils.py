import logging
from eg1.logger import logger

import time
import toml
from pathlib import Path
from requests import Response
from jinja2 import BaseLoader, Environment
from typing import Any
from itertools import product
import importlib
import pkgutil
import concurrent.futures
import functools

from ecologits.tracers.utils import compute_llm_impacts, electricity_mixes


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
    """Get a list of class obj from given package name and class_names.
    If `more` is given, it tries to extract the object with that names in the same module where a class is found.
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


#
# carbon emission in kgCO2e (use Ecologits for estimation)
#


def load_models_info() -> dict:
    config_path = Path("eg1/config/models-extra-info.toml")

    with open(config_path, "r", encoding="utf-8") as f:
        config = toml.load(f)

    return config


def get_model_name_from_path(full_name: str) -> str:
    return full_name.split("/")[-1].lower()


DEFAULT_PARAMS = {"params": 100, "active_params": 100, "total_params": 100}


def estimate_model_params(model_name: str) -> dict:
    """Estimate model parameters based on its name and known patterns."""
    name_lower = model_name.lower()

    # Size estimation patterns
    size_patterns = {"mini": 3, "small": 7, "medium": 13, "large": 70, "xl": 200, "xxl": 400}

    # Mixture of Experts patterns
    moe_patterns = ["moe", "mixture", "sparse"]
    # Total parameters estimation
    total_params = DEFAULT_PARAMS["total_params"]
    for pattern, size in size_patterns.items():
        if pattern in name_lower:
            total_params = size
            break

    # Active parameters estimation
    active_params = total_params
    if any(pattern in name_lower for pattern in moe_patterns):
        active_params = total_params // 4  # MoE models typically use 1/4 of total parameters

    return {
        "params": total_params,
        "total_params": total_params,
        "active_params": active_params,
        "estimated": True,
    }


def build_model_extra_info(model_name: str, models_info_params: dict) -> dict:
    """Build model information dictionary with default values for missing parameters."""
    std_name = get_model_name_from_path(model_name)
    logger.debug(f"Processing model: {std_name}")

    # Case-insensitive search in TOML keys
    model = None
    for key in models_info_params.keys():
        if key.lower() == std_name:
            model = models_info_params[key]
            break

    if model is None:
        logger.debug(f"Model {std_name} not found in models-extra-info.toml. Estimating parameters...")
        model = estimate_model_params(std_name)
        model["id"] = std_name.lower()
        model["organisation"] = "unknown"
        model["license"] = "unknown"
        model["description"] = f"Model {std_name} not found in configuration. Parameters are estimated."
    else:
        model = model.copy()
        model["id"] = model.get("id", std_name).lower()
        model["estimated"] = False

    # Handle size parameters
    if not any(model.get(key) for key in ("friendly_size", "params", "total_params")):
        model["params"] = 100

    # Map friendly sizes to parameter counts
    PARAMS_SIZE_MAP = {"XS": 3, "S": 7, "M": 35, "L": 70, "XL": 200}
    model["params"] = model.get("total_params", PARAMS_SIZE_MAP.get(model.get("friendly_size"), 100))

    # Calculate required RAM based on quantization
    if model.get("quantization", None) == "q8":
        model["required_ram"] = model["params"] * 2  # q8 quantization uses 2 bytes per parameter
    else:
        model["required_ram"] = model["params"]  # Default: 1 byte per parameter

    logger.debug(f"Model info: {model}")
    return model


def impact_carbon(model_name: str, model_url: str, token_count: int, request_latency: float) -> dict:
    """Calculate carbon impact of a model inference."""
    logger.debug(f"model_name : {model_name}")
    logger.debug(f"model_url : {model_url}")
    logger.debug(f"token_count : {token_count}")

    models_info = load_models_info()
    model_data = build_model_extra_info(model_name, models_info)

    # Validate input parameters
    if not isinstance(token_count, (int, float)) or token_count < 0:
        raise ValueError("token_count must be a positive number")
    if not isinstance(request_latency, (int, float)) or request_latency < 0:
        raise ValueError("request_latency must be a positive number")

    # Get model parameters
    mapc = model_data.get("active_params", model_data.get("params", 100))
    matpc = model_data.get("total_params", model_data.get("params", 100))

    # Determine electricity mix zone
    if not isinstance(model_url, str):
        raise ValueError("model_url must be a string")

    # Use French electricity mix for Albert models, world average for others
    electricity_mix_zone = "FRA" if "albert" in model_url.lower() else "WOR"
    electricity_mix = electricity_mixes.find_electricity_mix(zone=electricity_mix_zone)

    if not electricity_mix:
        raise ValueError(f"electricity zone {electricity_mix_zone} not found")

    # Calculate carbon impact using Ecologits
    impacts = compute_llm_impacts(
        model_active_parameter_count=mapc,
        model_total_parameter_count=matpc,
        output_token_count=token_count,
        if_electricity_mix_adpe=electricity_mix.adpe,
        if_electricity_mix_pe=electricity_mix.pe,
        if_electricity_mix_gwp=electricity_mix.gwp,
        request_latency=request_latency,
    )

    # Convert to dict and add estimation flag
    impacts_dict = impacts.model_dump()
    impacts_dict["estimated"] = model_data.get("estimated", False)

    return impacts_dict
