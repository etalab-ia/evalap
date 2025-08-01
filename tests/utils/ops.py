from fastapi.testclient import TestClient
from evalap.api.config import API_BASE_URL


ROOT_PATH = API_BASE_URL


def read_ops_metrics(client: TestClient):
    return client.get(f"{ROOT_PATH}/v1/ops_metrics")


def read_ops_eco(client: TestClient):
    return client.get(f"{ROOT_PATH}/v1/ops_eco")

