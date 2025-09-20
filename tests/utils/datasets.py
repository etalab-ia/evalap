import pandas as pd
from fastapi.testclient import TestClient

from evalap.api.config import API_BASE_URL

ROOT_PATH = API_BASE_URL


def read_datasets(client: TestClient):
    return client.get(f"{ROOT_PATH}/v1/datasets")


def read_dataset(client: TestClient, id: int, with_df: bool = False):
    params = {"with_df": with_df}
    return client.get(f"{ROOT_PATH}/v1/dataset/{id}", params=params)


def create_dataset(client: TestClient, params):
    params = params.copy()
    if "df" in params:
        if isinstance(params["df"], dict):
            params["df"] = pd.DataFrame(params["df"])
        params["df"] = params["df"].to_json()

    return client.post(f"{ROOT_PATH}/v1/dataset", json=params)
