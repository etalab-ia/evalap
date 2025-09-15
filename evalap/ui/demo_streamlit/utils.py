import json
import re
from collections import defaultdict
from copy import deepcopy
import pandas as pd
import requests
import streamlit as st
from typing import Optional
import hashlib

API_BASE_URL = "http://localhost:8000/v1"


def fetch(method, endpoint, data=None):
    func = getattr(requests, method)
    q = ""
    kw = {}
    if method == "get" and data:
        q = "?" + "&".join([f"{k}={v}" for k, v in data.items()])
    elif data:
        kw["json"] = data

    response = func(f"{API_BASE_URL}{endpoint}{q}", **kw)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data from {endpoint}.")
        return None


def hash_string(input_string, bits=8):
    hash_object = hashlib.sha256(input_string.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:bits]


def calculate_tokens_per_second(tokens: Optional[int], time: Optional[float]) -> Optional[float]:
    return round(tokens / time, 1) if tokens is not None and time is not None and time != 0 else None


def _all_equal(lst):
    return all(x == lst[0] for x in lst)


def _remove_commons_items(model_params: list[dict], first=True) -> list[dict]:
    if first:
        model_params = deepcopy(model_params)

    common_keys = set.intersection(*(set(d.keys()) for d in model_params))
    for k in common_keys:
        if _all_equal([d[k] for d in model_params]):
            _ = [d.pop(k) for d in model_params]
        elif all(isinstance(d[k], dict) for d in model_params):
            # improves: works with any instead of all
            # take all dict value (recurse)
            # reinsert dict value in same order
            x = [(i, d[k]) for i, d in enumerate(model_params) if isinstance(d[k], dict)]
            idx, params = zip(*x)
            params = _remove_commons_items(list(params), first=False)
            for i, _id in enumerate(idx):
                if not params[i]:
                    model_params[_id].pop(k)
                model_params[_id][k] = params[i]
        elif all(isinstance(d[k], list) for d in model_params):
            # @improves: works with any instead of all
            # take all dict value in  list value (recurse)
            # reinsert dict value in same order
            pass

    return model_params


def _rename_model_variants(experiments: list) -> list:
    """
    Inplace add a _name attribute to experiment when
    several model names are equal to help distinguish them.

    Note: Model.aliased_name will take precedence.
    """
    names = [expe["model"]["name"] for expe in experiments if expe.get("model")]
    if len(set(names)) == len(names):
        return experiments

    names = []
    for i, expe in enumerate(experiments):
        if not expe.get("model") or expe["model"].get("aliased_name"):
            continue

        name = expe["model"]["name"]
        _name = name
        suffix = ""
        if re.search(r"__\d+$", name):
            parts = name.rsplit("__", 1)
            _name = parts[0]
            suffix = parts[1]

        names.append(
            {
                "pos": i,
                "name": name,
                "_name": _name,
                "suffix": suffix,
            }
        )

    # Find the experiments that have an equal _model name
    model_names = defaultdict(list)
    for item in names:
        if not item:
            continue
        model_names[item["_name"]].append(item["pos"])

    # Canonize model names
    for _name, ids in model_names.items():
        if len(ids) <= 1:
            continue

        # List of model params
        model_params = [
            (experiments[id]["model"].get("sampling_params") or {})
            | (experiments[id]["model"].get("extra_params") or {})
            for id in ids
        ]

        # Manage system_prompt param by computing its hash
        for i, id in enumerate(ids):
            if not experiments[id]["model"].get("system_prompt"):
                continue
            model_params[i]["sys_prompt"] = hash_string(experiments[id]["model"]["system_prompt"], 4)

        # remove commons parameters
        model_diff_params = _remove_commons_items(model_params)

        for model in names:
            pos = next((x for x in ids if model["pos"] == x), None)
            if pos is None:
                continue

            # Finally renamed it !
            variant = model_diff_params[ids.index(pos)]
            if variant:
                variant = json.dumps(variant)
                variant = variant.replace('"', "").replace(" ", "")

                experiments[pos]["_model"] = "#".join([_name, variant]) + model["suffix"]


def _find_default_sort_metric(columns):
    """
    find a sensible default metric for sorting results.
    """
    preferred_metrics = ["judge_precision", "judge_notator", "answer_relevancy", "judge_exactness"]
    for metric in preferred_metrics:
        if metric in columns:
            return f"{metric}"

    return list(columns)[0] if len(columns) > 0 else None


def _extract_mean(value):
    try:
        return float(value.split("±")[0].strip())
    except:
        return value  # Return original value if not in expected format


def _sort_score_df(*dfs, reset_index=False):
    if len(dfs) == 0:
        return

    df = dfs[0]
    sorting_metric = _find_default_sort_metric(df.columns)
    df.sort_values(
        by=sorting_metric,
        key=lambda x: x.map(_extract_mean),
        ascending=False,
        inplace=True,
    )
    # Store the sorted index before resetting it
    sorted_idx = df.index.copy()
    for df in dfs:
        # Reorder df2 inplace to match df1's order
        df.loc[:] = df.loc[sorted_idx].values
        if reset_index:
            # Reset indices inplace
            df.reset_index(drop=True, inplace=True)


def _sort_columns(df: pd.DataFrame, first_columns: list) -> pd.DataFrame:
    first_columns = []
    new_column_order = sorted(first_columns) + sorted(  # Sort the first group of columns
        [col for col in df.columns if col not in first_columns]
    )  # Sort remaining columns
    return df[new_column_order]


def _check_repeat_mode(experiments: list) -> bool:
    """
    check whether the experiment is related to a repetition
    """
    for expe in experiments:
        name = expe["name"]
        if re.search(r"__\d+$", name):
            return True

    return False


def _format_model_params(expe):
    if not expe.get("model"):
        return None

    model = expe["model"].copy()
    model_params = (model.get("sampling_params") or {}) | (model.get("extra_params") or {})
    if model.get("system_prompt"):
        model_params["sys_prompt"] = hash_string(model["system_prompt"], 4)

    return model_params
