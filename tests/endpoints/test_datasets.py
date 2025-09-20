import pytest
from fastapi.testclient import TestClient

from tests.test_api import TestApi
from tests.utils import datasets, log_and_assert

dataset_cases = [
    {
        "name": "my_dataset",
        "readme": "I am a readme",
        "df": {"query": ["i am a query"] * 10, "column_xxx": [str(i) for i in range(10)]},
        "default_metric": "judge_xxx",
    },
]


class TestEndpointsDataset(TestApi):
    @pytest.mark.parametrize("dataset", dataset_cases)
    def test_dataset(self, client: TestClient, dataset):
        # Create dataset
        response = datasets.create_dataset(client, dataset)
        log_and_assert(response, 200)
        dataset_id = response.json()["id"]

        # Read dataset
        response = datasets.read_dataset(client, dataset_id, with_df=False)
        log_and_assert(response, 200)

        # Read dataset
        response = datasets.read_dataset(client, dataset_id, with_df=True)
        log_and_assert(response, 200)

        # Read datasets
        response = datasets.read_datasets(client)
        log_and_assert(response, 200)

    def test_read_dataset_not_found(self, client: TestClient):
        nonexistent_id = 99999
        response = datasets.read_dataset(client, nonexistent_id)
        log_and_assert(response, 404)
