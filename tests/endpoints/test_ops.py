import pytest
from fastapi.testclient import TestClient

from tests.test_api import TestApi
from tests.utils import ops, log_and_assert

ops_metrics_cases = [
    {
        "experiment_sets": 1,
        "unique_experiments": 2,
        "unique_answers": 3,
        "unique_metrics": 4,
        "unique_observations": 5,
        "distinct_models": ["model1", "model2"],
    },
    #ops metrics empty
    {
        "experiment_sets": 0,
        "unique_experiments": 0,
        "unique_answers": 0,
        "unique_metrics": 0,
        "unique_observations": 0,
        "distinct_models": [],
    },

]


def assert_ops_metrics_types(metrics_dict):
    assert isinstance(metrics_dict, dict)

    numeric_keys = [
        "experiment_sets",
        "unique_experiments",
        "unique_answers",
        "unique_metrics",
        "unique_observations",
    ]

    for key in numeric_keys:
        assert key in metrics_dict, f"Missing key in response: {key}"
        assert isinstance(metrics_dict[key],
                          (int, float)), f"The '{key}' field must be a float or int: {type(metrics_dict[key])}"

    assert "distinct_models" in metrics_dict
    assert isinstance(metrics_dict["distinct_models"], list), "'distinct_models' must be a list"
    for i, model in enumerate(metrics_dict["distinct_models"]):
        assert isinstance(model, str), f"Element {i} of 'distinct_models'is not a string"


class TestEndpointsOpsMetrics(TestApi):
    def test_read_ops_metrics(self, client: TestClient):
        response = ops.read_ops_metrics(client)
        log_and_assert(response, 200)
        data = response.json()
        assert_ops_metrics_types(data)


ops_eco_cases = [
    {'answers': {'total_emissions': {},
                 'total_entries_with_emissions': 3119,
                 'first_emission_date': '2025-06-12T17:30:24.745014'},
     'observation_table': {'total_emissions': {},
                           'total_entries_with_emissions': 0,
                           'first_emission_date': None}},

]

def assert_emissions_dict(emissions_dict):
    assert isinstance(emissions_dict, dict)
    for key, value in emissions_dict.items():
        assert isinstance(value, (float,
                                  int)), \
            f"The '{key}' field is not a float or int: {value} (type: {type(value)})"

class TestEndpointsOpsEco(TestApi):
    def test_read_eco_metrics(self, client: TestClient):
        response = ops.read_ops_eco(client)
        log_and_assert(response, 200)
        data = response.json()

        assert_emissions_dict(data['answers']['total_emissions'])
        assert isinstance(data['answers']['total_entries_with_emissions'], int)
        assert isinstance(data['answers']['first_emission_date'], str) or data['answers']['first_emission_date'] is None

        assert_emissions_dict(data['observation_table']['total_emissions'])
        assert isinstance(data['observation_table']['total_entries_with_emissions'], int)
        assert isinstance(data['observation_table']['first_emission_date'], str) or data['observation_table'][
            'first_emission_date'] is None
