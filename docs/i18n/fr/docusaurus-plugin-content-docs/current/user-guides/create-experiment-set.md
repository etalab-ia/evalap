---
sidebar_position: 3
---

# Créer un ensemble d'expériences

Ce guide explique comment créer et exécuter une évaluation d'ensemble d'expériences dans EvalAP, ce qui vous permet de comparer plusieurs modèles ou configurations.

> **Note :** Avant de poursuivre avec ce guide, assurez-vous d'avoir lu l'article [Créer une expérience simple](create-a-simple-experiment), car il couvre les concepts fondamentaux nécessaires pour comprendre les ensembles d'expériences.

## Pourquoi utiliser des ensembles d'expériences ?

Les évaluations significatives consistent rarement en une seule expérience. Pour tirer des conclusions valides sur les performances d'un modèle, vous avez besoin de :

1. **Analyse comparative** : Comparer différents modèles sur le même jeu de données
2. **Reproductibilité** : Exécuter la même expérience plusieurs fois pour tenir compte de la variabilité
3. **Exploration des paramètres** : Tester comment différentes configurations affectent les performances
4. **Évaluation complète** : Évaluer les modèles sur plusieurs métriques

Les ensembles d'expériences dans EvalAP facilitent l'organisation d'expériences connexes et l'analyse collective de leurs résultats.

## Créer un ensemble d'expériences via l'API

Il existe deux façons principales de créer un ensemble d'expériences :

1. **Schéma de validation croisée (CV)** : Générer automatiquement des expériences en combinant des paramètres
2. **Définition manuelle** : Définir explicitement chaque expérience dans l'ensemble

### Utilisation du schéma de validation croisée

Le schéma CV est puissant pour générer plusieurs expériences à partir d'une grille de paramètres :

```python
import os
import requests

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Define your experiment set with CV schema
expset_name = "model_comparison_v1"
expset_readme = "Comparing performance of various LLMs on a QA dataset."
metrics = ["judge_precision", "output_length", "generation_time"]

# Parameters common to all experiments
common_params = {
    "dataset": "qa_benchmark_v2",  # assuming this dataset has been added before
    "model": {"sampling_params": {"temperature": 0.2}},
    "metrics": metrics,
    "judge_model": "gpt-4o",
}

# Parameters that will vary across experiments
grid_params = {
    "model": [
        {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
        {"name": "claude-3-opus-20240229", "base_url": "https://api.anthropic.com", "api_key": os.getenv("ANTHROPIC_API_KEY")},
        {"name": "google/gemma-2-9b-it", "base_url": "https://api.albert.fr/v1", "api_key": os.getenv("ALBERT_API_KEY")},
        {"name": "meta-llama/Llama-3.1-8B-Instruct", "base_url": "https://api.albert.fr/v1", "api_key": os.getenv("ALBERT_API_KEY")},
    ],
}

# Create the experiment set with CV schema
expset = {
    "name": expset_name,
    "readme": expset_readme,
    "cv": {
        "common_params": common_params, 
        "grid_params": grid_params, 
        "repeat": 3  # Run each combination 3 times to measure variability
    }
}

# Launch the experiment set
response = requests.post(f'{API_URL}/experiment_set', json=expset, headers=HEADERS)
expset_id = response.json()["id"]
print(f"Experiment set {expset_id} is running")
```

Dans cet exemple :
- `common_params` définit les paramètres partagés entre toutes les expériences
- `grid_params` définit les paramètres qui varieront (créant une expérience séparée pour chaque combinaison)
- `repeat` spécifie combien de fois répéter chaque expérience (utile pour mesurer la variabilité)

L'API générera automatiquement des expériences pour toutes les combinaisons de paramètres dans la grille.

### Définir manuellement les expériences

Pour plus de contrôle, vous pouvez définir explicitement chaque expérience dans l'ensemble :

```python
import os
import requests

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Define your experiment set with explicit experiments
expset = {
    "name": "custom_evaluation_set",
    "readme": "Custom evaluation with different configurations for each model.",
    "experiments": [
        {
            "name": "gpt4o_standard",
            "dataset": "qa_benchmark_v2",
            "model": {
                "name": "gpt-4o", 
                "base_url": "https://api.openai.com/v1", 
                "api_key": os.getenv("OPENAI_API_KEY"),
                "sampling_params": {"temperature": 0.0}
            },
            "metrics": ["judge_precision", "output_length"]
        },
        {
            "name": "gpt4o_creative",
            "dataset": "qa_benchmark_v2",
            "model": {
                "name": "gpt-4o", 
                "base_url": "https://api.openai.com/v1", 
                "api_key": os.getenv("OPENAI_API_KEY"),
                "sampling_params": {"temperature": 0.7}
            },
            "metrics": ["judge_precision", "output_length"]
        },
        {
            "name": "llama3_with_rag",
            "dataset": "qa_benchmark_v2",
            "model": {
                "name": "meta-llama/Llama-3.1-8B-Instruct",
                "base_url": "https://api.custom.fr/v1",
                "api_key": os.getenv("CUSTOM_API_KEY"),
                "extra_params": {"rag": {"mode": "rag", "limit": 5}}
            },
            "metrics": ["judge_precision", "output_length", "contextual_relevancy"]
        }
    ]
}

# Launch the experiment set
response = requests.post(f'{API_URL}/experiment_set', json=expset, headers=HEADERS)
expset_id = response.json()["id"]
print(f"Experiment set {expset_id} is running")
```

Cette approche vous donne une flexibilité complète pour personnaliser chaque expérience indépendamment.

## Cas d'usage avancés

Les ensembles d'expériences sont particulièrement utiles pour :

1. **Comparaison de modèles** : Évaluer plusieurs modèles sur le même jeu de données pour identifier le plus performant
2. **Ajustement des hyperparamètres** : Tester comment des paramètres comme la température affectent les sorties du modèle
3. **Test de robustesse** : Exécuter la même expérience plusieurs fois pour mesurer la cohérence
4. **Évaluation des fonctionnalités** : Comparer des modèles avec et sans fonctionnalités comme le RAG pour mesurer l'impact

## Visualiser les résultats d'un ensemble d'expériences

Après avoir lancé un ensemble d'expériences :

1. Naviguez vers la page de détails de l'ensemble d'expériences
2. Consultez les résultats récapitulatifs montrant :
    - Les performances comparatives de toutes les expériences
    - Les mesures statistiques de variabilité lors de l'utilisation d'exécutions répétées
3. Explorez les résultats détaillés pour chaque expérience individuelle
4. Générez des graphiques de comparaison et des visualisations

Les ensembles d'expériences fournissent une vue complète des performances des modèles, facilitant ainsi la formulation de conclusions significatives à partir de vos évaluations.


:::tip Prochaines étapes : Ensembles d'expériences
[Explorez les notebooks pour des exemples réels de création d'évaluations avec des ensembles d'expériences.](https://github.com/etalab-ia/evalap/tree/main/notebooks)
:::
