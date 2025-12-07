---
sidebar_position: 4
---

# Utilisez votre propre prompt personnalisé pour LLM-as-a-Judge

Ce guide explique comment utiliser des prompts personnalisés pour l'évaluation LLM-as-a-judge dans EvalAP en utilisant des métriques paramétrées.

## Comprendre les métriques paramétrées

EvalAP prend en charge deux types de métriques lors de la conception d'une expérience :

1. **Métriques non paramétrées** (chaîne de caractères) : Noms de métriques simples comme `"judge_precision"` ou `"generation_time"`
2. **Métriques paramétrées** (dictionnaire) : Métriques qui acceptent des paramètres personnalisés pour un contrôle plus fin

Les métriques paramétrées vous permettent de personnaliser le comportement des métriques en transmettant des options de configuration supplémentaires. Ceci est particulièrement utile lorsque vous souhaitez utiliser vos propres prompts d'évaluation au lieu de ceux par défaut.

## Structure d'une métrique paramétrée

Une métrique paramétrée est définie comme un dictionnaire avec trois champs :

| Champ | Type | Description |
|-------|------|-------------|
| `name` | string | L'identifiant de la métrique à utiliser |
| `aliased_name` | string | Un nom d'affichage personnalisé affiché dans le frontend |
| `params` | object | Un objet contenant les paramètres requis et optionnels de la métrique |

## Utilisation de prompts de juge personnalisés avec `judge_adhoc`

La métrique `judge_adhoc` vous permet de définir vos propres critères d'évaluation LLM-as-a-judge en utilisant un prompt personnalisé.

### Paramètres requis

| Paramètre | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Votre prompt d'évaluation personnalisé pour le modèle juge |

### Exemple : Juge personnalisé simple

Voici comment créer une expérience avec un prompt de juge personnalisé :

```python
import os
import requests

API_URL = "https://evalap.etalab.gouv.fr/v1"
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Définir un prompt de juge personnalisé
custom_prompt = """Évaluez si la réponse est polie et professionnelle.
Retournez 1 si la réponse répond aux deux critères, 0 sinon.

Question : {query}
Réponse : {output}
"""

# Concevoir l'expérience avec une métrique paramétrée
experiment = {
    "name": "politeness_evaluation",
    "dataset": "my_dataset",
    "model": {
        "name": "gpt-4o",
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY")
    },
    "metrics": [
        # Métrique non paramétrée (chaîne)
        "generation_time",
        # Métrique paramétrée (dictionnaire)
        {
            "name": "judge_adhoc",
            "aliased_name": "Score de Politesse",
            "params": {
                "prompt": custom_prompt
            }
        }
    ]
}

# Lancer l'expérience
response = requests.post(f'{API_URL}/experiment', json=experiment, headers=HEADERS)
experiment_id = response.json()["id"]
print(f"L'expérience {experiment_id} est en cours d'exécution")
```

### Exemple : Plusieurs juges personnalisés

Vous pouvez utiliser plusieurs métriques paramétrées dans la même expérience, chacune avec des prompts personnalisés différents :

```python
# Définir plusieurs prompts de juge personnalisés
accuracy_prompt = """Évaluez si la réponse répond correctement à la question.
Retournez 1 si précise, 0 sinon.

Question : {query}
Réponse : {output}
Attendu : {output_true}
"""

clarity_prompt = """Évaluez si la réponse est claire et facile à comprendre.
Retournez 1 si claire, 0 sinon.

Réponse : {output}
"""

experiment = {
    "name": "multi_criteria_evaluation",
    "dataset": "my_dataset",
    "model": {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
    "metrics": [
        {
            "name": "judge_adhoc",
            "aliased_name": "Précision",
            "params": {"prompt": accuracy_prompt}
        },
        {
            "name": "judge_adhoc",
            "aliased_name": "Clarté",
            "params": {"prompt": clarity_prompt}
        },
        "generation_time"
    ]
}
```

## Variables disponibles dans les prompts personnalisés

Votre prompt personnalisé peut référencer des colonnes de jeux de données et des sorties de modèle en utilisant des variables de template. Les variables courantes incluent :

- `{query}` : La requête d'entrée de votre jeu de données
- `{output}` : La réponse générée par le modèle
- `{output_true}` : La réponse de référence (si disponible dans votre jeu de données)
- `{context}` : Contexte supplémentaire fourni au modèle
- `{retrieval_context}` : Informations récupérées utilisées lors de la génération

Assurez-vous que toutes les variables que vous référencez dans votre prompt correspondent à des colonnes de votre jeu de données ou à des champs générés pendant l'évaluation.

:::tip Configuration du modèle juge
Par défaut, les prompts de juge personnalisés utilisent le modèle juge configuré d'EvalAP. Vous pouvez spécifier un modèle juge différent en utilisant le paramètre `judge_model` au niveau de l'expérience, comme décrit dans le guide [Créer une expérience simple](./create-a-simple-experiment#configuring-a-llm-as-a-judge-model).
:::

## Mélanger les métriques paramétrées et non paramétrées

Vous pouvez librement mélanger les deux types de métriques dans votre expérience :

```python
experiment = {
    "name": "mixed_metrics_experiment",
    "dataset": "my_dataset",
    "model": {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
    "metrics": [
        # Métriques standard (non paramétrées)
        "generation_time",
        "output_length",
        "judge_precision",
        # Métrique de juge personnalisée (paramétrée)
        {
            "name": "judge_adhoc",
            "aliased_name": "Évaluation Personnalisée",
            "params": {
                "prompt": "Votre prompt personnalisé ici..."
            }
        }
    ]
}
```

:::info
Le champ `aliased_name` est particulièrement utile lors de l'utilisation de plusieurs instances de la même métrique avec des paramètres différents, car il aide à les distinguer dans la vue des résultats du frontend.
:::
