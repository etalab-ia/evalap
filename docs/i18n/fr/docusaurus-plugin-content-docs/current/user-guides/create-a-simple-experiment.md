---
sidebar_position: 2
---

# Créer une Expérience Simple

Ce guide vous accompagne dans la création et l'exécution d'une expérience d'évaluation simple dans Evalap.

## Créer une Expérience via l'API

Une expérience évalue un modèle sur un jeu de données spécifique en utilisant des métriques définies.

Lors du choix d'un modèle, il existe généralement deux scénarios :
1. **Modèles de fournisseurs** (par exemple, OpenAI, Albert) : EvalAP génère des réponses à partir du jeu de données. Le jeu de données doit contenir au moins une colonne `query` représentant les entrées du modèle.
2. **Modèles personnalisés** : Vous générez vous-même les sorties du modèle et les transmettez à l'API pour le calcul des métriques.

Ce guide couvre les deux scénarios.

### Sélection des Métriques

Vous devez spécifier quelles métriques calculer pour votre expérience. Vous pouvez explorer les métriques disponibles via l'interface ou l'API.

Une métrique typique pour évaluer les LLM est "LLM-as-a-judge", qui utilise un autre LLM pour évaluer la qualité des réponses. Lorsque vous avez des réponses de référence dans votre jeu de données, vous pouvez utiliser LLM-as-a-judge pour vérifier si la sortie du modèle contient la bonne réponse. Dans EvalAP, la métrique `judge_precision` remplit cette fonction.

Voici quelques métriques clés offertes par EvalAP :

| Name                      | Description                                                                                                      | Type     | Require                                      |
|---------------------------|------------------------------------------------------------------------------------------------------------------|----------|----------------------------------------------|
| judge_precision           | Binary precision of output_true. Returns 1 if the correct answer is contained in the given answer                | llm      | [output, output_true, query]                 |
| qcm_exactness             | Binary equality between output and output_true                                                                   | llm      | [output, output_true]                        |
| bias                      | See https://docs.confident-ai.com/docs/metrics-introduction                                                     | deepeval | [output, query]                              |
| hallucination             | See https://docs.confident-ai.com/docs/metrics-introduction                                                     | deepeval | [context, output, query]                     |
| contextual_relevancy      | See https://docs.confident-ai.com/docs/metrics-introduction                                                     | deepeval | [output, query, retrieval_context]           |
| ocr_v1                    | Levenshtein distance between output and ground-truth markdown                                                    | ocr      | [output, output_true]                        |
| output_length             | Number of words in the output                                                                                   | ops      | [output]                                     |
| generation_time           | Time taken to generate the answer/output                                                                        | ops      | [output]                                     |
| energy_consumption        | Energy consumption (kWh) - Environmental impact calculated by ecologits library                                  | ops      | [output]                                     |
| nb_tool_calls             | Number of tools called during generation                                                                         | ops      | [output]                                     |

:::info
Consultez la liste complète des métriques depuis la route API [v1/metrics](https://evalap.etalab.gouv.fr/redoc#tag/metrics).
:::

Lors de la sélection des métriques, assurez-vous que les champs requis correspondent aux colonnes de votre jeu de données. Par exemple, `judge_precision` nécessite les champs `output`, `output_true` et `query`. Notez que le champ `output` est généré par EvalAP pendant l'évaluation, il n'a donc pas besoin d'être présent dans votre jeu de données initialement.

Des métriques supplémentaires fournissent des mesures générales comme le temps de génération et la taille de sortie.

### Créer une Expérience avec un Fournisseur de Modèle

Voici comment créer une expérience simple évaluant un modèle OpenAI :

```python
import os
import requests

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token (or None if launch locally)
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Design the experiment
experiment = {
    "name": "my_experiment_name", 
    "dataset": "my_dataset", # name identifier of the dataset
    "model": {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
    "metrics": ["judge_precision", "generation_time", "output_length"],
}

# Run the experiment
response = requests.post(f'{API_URL}/experiment', json=experiment, headers=HEADERS)
experiment_id = response.json()["id"]
print(f"Experiment {experiment_id} is running")
```

:::info
Le schéma du modèle prend en charge le passage de paramètres d'échantillonnage, comme la température avec `"model": {..., "sampling_params": {"temperature": 0.2}}`, ou des paramètres supplémentaires pris en charge par l'API Openai utilisée. Consultez le [point de terminaison de création d'expérience](https://evalap.etalab.gouv.fr/redoc#tag/experiments/operation/create_experiment_v1_experiment_post) pour la liste complète des paramètres pris en charge.
:::

### Créer une Expérience avec un Modèle Personnalisé

Pour le second scénario, où vous avez vos propres sorties de modèle, vous devrez fournir ces sorties dans votre appel API. Voici comment créer une expérience avec un modèle personnalisé :

```python
import os
import requests

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token (or None if launch locally)
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Design the experiment with a custom model
experiment = {
    "name": "my_custom_model_experiment", 
    "dataset": "my_dataset", # name identifier of the dataset
    "model": {
        "aliased_name": "my-custom-model",  # A name to identify this model
        "output": ["answer1", "answer2", "answer3"]  # Array of model outputs corresponding to dataset rows
    },
    "metrics": ["judge_precision", "generation_time", "output_length"],
}

# Run the experiment
response = requests.post(f'{API_URL}/experiment', json=experiment, headers=HEADERS)
experiment_id = response.json()["id"]
print(f"Experiment {experiment_id} is running")
```

Dans ce scénario, le schéma du modèle est différent :

| Field | Type | Description |
|-------|------|-------------|
| output | Array of strings | The sequence of answers generated by your model, ordered to match the 'rows' of the dataset you are evaluating |
| aliased_name | string | A name to identify this model. Different from the 'name' parameter used with provider models |

Après avoir exécuté l'expérience, l'API renvoie une réponse de succès si elle démarre sans erreurs. EvalAP gère les expériences de manière asynchrone, et vous pouvez vérifier l'état et les résultats via l'interface ou en interrogeant directement l'API.


### Configuration d'un Modèle LLM-as-a-Judge

Lorsque vous utilisez des métriques comme `judge_precision` qui s'appuient sur un LLM pour évaluer les sorties, vous pouvez personnaliser le modèle qui agit comme juge. Par défaut, EvalAP utilise un petit modèle préconfiguré, mais vous pouvez spécifier le vôtre en utilisant le paramètre `judge_model` dans votre configuration d'expérience.

Vous pouvez spécifier le modèle juge de deux façons :

1. **En utilisant une chaîne de caractères pour le nom du modèle** : EvalAP utilisera le premier modèle disponible correspondant à ce nom parmi vos fournisseurs configurés (Pour configurer un fournisseur, vous devez simplement avoir la clé API appropriée définie dans votre environnement avant de lancer EvalAP, par exemple `OPENAI_API_KEY`, `MISTRAL_API_KEY`).
2. **En utilisant une configuration complète du modèle** : Fournissez le nom du modèle, l'URL de base et la clé API.


Voici un exemple d'utilisation :

```python
# En utilisant une chaîne de caractères pour le nom du modèle
experiment = {
    "name": "judge_precision",
    "dataset": "my_dataset",
    "model": {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
    "metrics": ["judge_precision", "generation_time"],
    "judge_model": "gpt-4-turbo"  # Spécifiez quel modèle utiliser comme juge
}

# Ou en utilisant une configuration complète du modèle
experiment = {
    "name": "judge_precision",
    "dataset": "my_dataset",
    "model": {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
    "metrics": ["judge_precision", "generation_time"],
    "judge_model": {
        "name": "claude-3-opus-20240229",
        "base_url": "https://api.anthropic.com/v1",
        "api_key": os.getenv("ANTHROPIC_API_KEY")
    }
}

## Consulter les Résultats et la Progression de l'Expérience

Après avoir lancé une expérience :

1. Naviguez vers la page de détails de l'expérience
2. Consultez les résultats sommaires montrant :
   - Les métriques de performance globales pour chaque modèle
   - Un tableau de support affichant le nombre d'expériences utilisées pour le calcul des moyennes
3. Explorez les résultats détaillés :
   - Nombre de tentatives réussies et échouées par expérience
   - Résultats détaillés pour chaque expérience


:::tip Next Steps: Experiment Sets
Après avoir créé votre première expérience, envisagez d'utiliser les **Ensembles d'Expériences** pour comparer plusieurs modèles ou configurations. Les ensembles d'expériences vous permettent d'exécuter des expériences connexes ensemble, facilitant ainsi les comparaisons significatives et les conclusions. Ils sont essentiels pour des évaluations robustes qui tiennent compte de la variabilité des modèles et fournissent des aperçus comparatifs. En savoir plus dans notre guide [Créer un Ensemble d'Expériences](./create-experiment-set).
:::

