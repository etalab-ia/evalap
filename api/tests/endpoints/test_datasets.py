import pytest
from fastapi.testclient import TestClient

from api.tests.utils import datasets 
from api.tests.test_api import TestApi
import pandas as pd

class TestEndpointsDataset(TestApi):
    @pytest.mark.asyncio
    def test_create_dataset_without_output(self, client: TestClient):
        test_df = pd.DataFrame({
            'query': [1, 2],
            'colonne2': ['A', 'B']
        })
        
        response = datasets.create_dataset(
            client=client,
            name_dataset="test_dataset",
            df=test_df,
            readme="dataset de test",
            default_metric="test_metric"
        )
        
        assert response.status_code == 200
    
    def test_create_dataset_with_output(self, client: TestClient):
        test_df = pd.DataFrame({
            'query': [1, 2],
            'output': ['A', 'B']
        })
        
        response = datasets.create_dataset(
            client=client,
            name_dataset="test_dataset",
            df=test_df,
            readme="dataset de test",
            default_metric="test_metric"
        )
        
        assert response.status_code == 200

    def test_read_dataset(self, client: TestClient):
        response = datasets.read_dataset(client)
        print("response: ", response)
        assert response.status_code == 200

