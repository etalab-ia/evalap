import pytest
from unittest.mock import patch, MagicMock
from tests.test_api import TestApi

import eg1.utils_eco

# Mocks pour les dépendances externes
MOCK_MODELS_INFO = {
    "albert": {"params": 123, "total_params": 123, "active_params": 100, "id": "albert"},
    "other": {"params": 234, "total_params": 234, "active_params": 200, "id": "other"},
}
MOCK_ELECTRICITY_MIX = MagicMock(adpe=1.0, pe=2.0, gwp=3.0)
MOCK_IMPACT_RESULT = MagicMock(model_dump=lambda: {"gwp": 42, "adpe": 1, "pe": 2})


class TestEcoCarbon(TestApi):
    @patch("eg1.utils_eco.load_models_info", return_value=MOCK_MODELS_INFO)
    @patch("eg1.utils_eco.electricity_mixes.find_electricity_mix", return_value=MOCK_ELECTRICITY_MIX)
    @patch("eg1.utils_eco.compute_llm_impacts", return_value=MOCK_IMPACT_RESULT)
    def test_impact_carbon_albert(self, mock_compute, mock_elec, mock_models):
        result = eg1.utils_eco.impact_carbon("albert", "https://modelhost/albert", 50, 0.5)
        assert result["gwp"] == 42
        assert result["adpe"] == 1
        assert result["pe"] == 2
        assert result["estimated"] is False
        mock_elec.assert_called_with(zone="FRA")
        mock_compute.assert_called_once()

    @patch("eg1.utils_eco.load_models_info", return_value=MOCK_MODELS_INFO)
    @patch("eg1.utils_eco.electricity_mixes.find_electricity_mix", return_value=MOCK_ELECTRICITY_MIX)
    @patch("eg1.utils_eco.compute_llm_impacts", return_value=MOCK_IMPACT_RESULT)
    def test_impact_carbon_other_model(self, mock_compute, mock_elec, mock_models):
        result = eg1.utils_eco.impact_carbon("other", "https://modelhost/other", 100, 1.0)
        assert result["gwp"] == 42
        assert result["estimated"] is False
        mock_elec.assert_called_with(zone="WOR")

    @patch("eg1.utils_eco.load_models_info", return_value={})
    @patch("eg1.utils_eco.electricity_mixes.find_electricity_mix", return_value=MOCK_ELECTRICITY_MIX)
    @patch("eg1.utils_eco.compute_llm_impacts", return_value=MOCK_IMPACT_RESULT)
    def test_impact_carbon_estimation(self, mock_compute, mock_elec, mock_models):
        result = eg1.utils_eco.impact_carbon("unknown-model-large", "https://modelhost/unknown", 10, 0.1)
        assert result["estimated"] is True
        assert result["gwp"] == 42

    @patch("eg1.utils_eco.load_models_info", return_value=MOCK_MODELS_INFO)
    @patch("eg1.utils_eco.electricity_mixes.find_electricity_mix", return_value=MOCK_ELECTRICITY_MIX)
    @patch("eg1.utils_eco.compute_llm_impacts", return_value=MOCK_IMPACT_RESULT)
    def test_impact_carbon_token_count_invalid(self, mock_compute, mock_elec, mock_models):
        with pytest.raises(ValueError):
            eg1.utils_eco.impact_carbon("albert", "https://modelhost/albert", -1, 0.1)

    @patch("eg1.utils_eco.load_models_info", return_value=MOCK_MODELS_INFO)
    @patch("eg1.utils_eco.electricity_mixes.find_electricity_mix", return_value=MOCK_ELECTRICITY_MIX)
    @patch("eg1.utils_eco.compute_llm_impacts", return_value=MOCK_IMPACT_RESULT)
    def test_impact_carbon_latency_invalid(self, mock_compute, mock_elec, mock_models):
        with pytest.raises(ValueError):
            eg1.utils_eco.impact_carbon("albert", "https://modelhost/albert", 10, -0.1)

    @patch("eg1.utils_eco.load_models_info", return_value=MOCK_MODELS_INFO)
    @patch("eg1.utils_eco.electricity_mixes.find_electricity_mix", return_value=None)
    @patch("eg1.utils_eco.compute_llm_impacts", return_value=MOCK_IMPACT_RESULT)
    def test_impact_carbon_electricity_zone_not_found(self, mock_compute, mock_elec, mock_models):
        with pytest.raises(ValueError):
            eg1.utils_eco.impact_carbon("albert", "https://modelhost/albert", 10, 0.1)

    @patch("eg1.utils_eco.load_models_info", return_value=MOCK_MODELS_INFO)
    @patch("eg1.utils_eco.electricity_mixes.find_electricity_mix", return_value=MOCK_ELECTRICITY_MIX)
    @patch("eg1.utils_eco.compute_llm_impacts", return_value=MOCK_IMPACT_RESULT)
    def test_impact_carbon_model_url_not_string(self, mock_compute, mock_elec, mock_models):
        with pytest.raises(ValueError):
            eg1.utils_eco.impact_carbon("albert", 12345, 10, 0.1)
