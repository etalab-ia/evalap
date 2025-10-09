import pytest
from fastapi.testclient import TestClient

from tests.test_api import TestApi
from tests.utils import datasets, expsets, log_and_assert

dataset_cases = [
    {
        "name": "my_dataset",
        "readme": "I am a readme",
        "df": {"query": ["i am a query"] * 10, "output_true": ["A"] * 10},
        "default_metric": "judge_notator",
    },
]

expset_cases = [
    # Run two expe using using basic experiments definition
    {
        "name": "an expeset name",
        "readme": "I an expset readme",
        "experiments": [
            {
                "name": f"an experiment name {i}",
                "model": {"name": "x", "base_url": "x", "api_key": "x"},
                "metrics": ["judge_notator", "output_length", "generation_time"],
            }
            for i in range(2)
        ],
    },
    # Run multiple experiment using grid_search (cv) definitions
    {
        "name": "an expeset name",
        "readme": "I an expset readme",
        "cv": {
            "common_params": {
                "metrics": ["output_length", "generation_time"],
                "model": {"sampling_params": {"temperature": 1}},
            },
            "grid_params": {
                "model": [
                    {"name": "my/model1", "base_url": "x", "api_key": "x"},
                    {"name": "my/model2", "base_url": "x", "api_key": "x"},
                ],
            },
        },
    },
    # Run multiple experiment using grid_search (cv) definitions
    # - with ModelRaw
    {
        "name": "an expeset name",
        "readme": "I an expset readme",
        "cv": {
            "common_params": {
                "metrics": ["output_length", "generation_time"],
                "model": {"sampling_params": {"temperature": 1}},
            },
            "grid_params": {
                "model": [
                    {"aliased_name": "my_model1", "output": ["my answer"] * 10},
                    {"aliased_name": "my_model2", "output": ["my answer"] * 10},
                ],
            },
        },
    },
]


class TestEndpointsExperimentSet(TestApi):
    @pytest.mark.parametrize("dataset", dataset_cases)
    @pytest.mark.parametrize("expset", expset_cases)
    def test_experimentset(self, client: TestClient, dataset, expset):
        # Create dataset
        response = datasets.create_dataset(client, dataset)
        log_and_assert(response, 200)

        # Set the dataset name
        if expset.get("experiments"):
            for expe in expset["experiments"]:
                expe["dataset"] = dataset["name"]
        elif expset.get("cv"):
            if "model" not in expset["cv"]["common_params"]:
                expset["cv"]["common_params"]["model"] = {}
            expset["cv"]["common_params"]["dataset"] = dataset["name"]

        # Create expset
        response = expsets.create_experimentset(client, expset)
        log_and_assert(response, 200)
        expset_id = response.json()["id"]

        # Read first experiment set
        response = expsets.read_experimentset(client, expset_id)
        log_and_assert(response, 200)

        # Patch expset
        if expset.get("experiments"):
            # Respect the unique constraint on expe names
            for i, expe in enumerate(expset["experiments"]):
                expe["name"] = expe["name"] + str(i)
        response = expsets.patch_experimentset(client, expset_id, params=expset)
        log_and_assert(response, 200)

        # Delete expset

    def test_schema(self, client: TestClient):
        # TODO: write test for:
        # test parametrized metric (and required paremeters errors
        pass
