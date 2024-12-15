import requests

from api.config import API_BASE_URL


def get_experiment_sets():
    response = requests.get(f'{API_BASE_URL}/v1/experimentsets')
    response.raise_for_status()
    return response.json()


def delete_experiment_set(set_id):
    response = requests.delete(f'{API_BASE_URL}/v1/experimentset/{set_id}')
    response.raise_for_status()
    return response


def get_experiments(set_id):
    response = requests.get(f'{API_BASE_URL}/v1/experiments?set_id={set_id}')
    response.raise_for_status()
    return response.json()


def get_metrics():
    response = requests.get(f'{API_BASE_URL}/v1/metrics')
    response.raise_for_status()
    return response.json()


def get_datasets():
    response = requests.get(f'{API_BASE_URL}/v1/datasets')
    response.raise_for_status()
    return response.json()


def get_models():
    response = requests.get(f'{API_BASE_URL}/v1/models')
    response.raise_for_status()
    return response.json()
