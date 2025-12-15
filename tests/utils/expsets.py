from fastapi.testclient import TestClient

from evalap.api.config import API_BASE_URL

ROOT_PATH = API_BASE_URL


def read_experimentset(client: TestClient, id: int):
    params = {}
    return client.get(f"{ROOT_PATH}/v1/experiment_set/{id}", params=params)


def create_experimentset(client: TestClient, params):
    return client.post(f"{ROOT_PATH}/v1/experiment_set", json=params)


def stop_experimentset(client: TestClient, expset_id):
    return client.post(f"{ROOT_PATH}/v1/stop/experiment_set/{expset_id}")


def patch_experimentset(client: TestClient, expset_id, params):
    return client.patch(f"{ROOT_PATH}/v1/experiment_set/{expset_id}", json=params)
