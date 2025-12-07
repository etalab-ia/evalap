---
sidebar_position: 1
---

# Ajouter une Nouvelle Métrique

Ce guide vous accompagnera dans le processus d'ajout d'une métrique d'évaluation personnalisée à Evalap.

## Comprendre les Métriques dans Evalap

Evalap utilise un système de registre de métriques où les métriques sont enregistrées à l'aide de décorateurs. Il existe trois types de métriques :

- **Métriques LLM-as-judge** : Utilisent des modèles de langage pour évaluer les sorties
- **Métriques DeepEval** : S'intègrent avec la bibliothèque DeepEval
- **Métriques humaines** : Pour l'évaluation avec intervention humaine

Chaque métrique spécifie ses entrées requises et renvoie un score ainsi qu'une explication.

## Prérequis

Avant d'ajouter une nouvelle métrique, assurez-vous d'avoir :

- Un environnement de développement local configuré
- Une compréhension de la métrique que vous souhaitez implémenter
- Des connaissances de base en Python et sur les décorateurs

## Exemple 1 : Créer une Métrique LLM-as-Judge

Cet exemple montre comment créer une métrique qui utilise un LLM pour évaluer les sorties. Créez un nouveau fichier Python dans le répertoire `evalap/api/metrics/` :

```python
# evalap/api/metrics/my_custom_metric.py

from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

from . import metric_registry

# Define your prompt template for the LLM-as-judge metric
_template = """
Given the following question:

<question>
{{query}}
</question>

And the expected answer:

<expected>
{{output_true}}
</expected>

And the actual answer to evaluate:

<actual>
{{output}}
</actual>

Evaluate how well the actual answer matches the expected answer.
Score from 0 to 1, where 1 is a perfect match.

Return only the numeric score!
""".strip()

# Configuration for LLM-as-judge metrics
_config = {
    "model": "gpt-4o",
    "sampling_params": {"temperature": 0.2},
}

@metric_registry.register(
    name="my_custom_metric",
    description="Evaluates how well the output matches the expected answer",
    metric_type="llm",  # or "deepeval" or "human"
    require=["output", "output_true", "query"],  # Required inputs
)
def my_custom_metric(output, output_true, **kwargs):
    """
    Compute the custom metric score.

    Args:
        output: The model's output to evaluate
        output_true: The expected/reference output
        **kwargs: Additional parameters (e.g., query, context)

    Returns:
        tuple: (score, observation) where score is numeric and observation is explanation
    """
    # For LLM-as-judge metrics
    config = _config | {k: v for k, v in kwargs.items() if k in _config}

    messages = [
        {
            "role": "user",
            "content": render_jinja(_template, output=output, output_true=output_true, **kwargs),
        }
    ]

    aiclient = LlmClient()
    result = aiclient.generate(
        model=config["model"],
        messages=messages,
        **config["sampling_params"]
    )

    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)

    # Parse the score
    score = answer.strip(" \n\"'.%")
    try:
        score = float(score)
    except ValueError:
        score = None

    return score, observation
```

## Exemple 2 : Créer une Métrique Non-LLM

Cet exemple démontre comment créer une métrique simple qui n'utilise pas un LLM pour l'évaluation. Ces métriques utilisent une logique déterministe ou des calculs mathématiques :

```python
# evalap/api/metrics/exact_match.py

from . import metric_registry

@metric_registry.register(
    name="exact_match",
    description="Binary metric that checks if output exactly matches expected",
    metric_type="llm",  # Even simple metrics can be marked as "llm" type
    require=["output", "output_true"],
)
def exact_match_metric(output, output_true, **kwargs):
    """Check if output exactly matches expected output."""
    # Normalize strings for comparison
    output_normalized = output.strip().lower()
    expected_normalized = output_true.strip().lower()

    # Calculate score
    score = 1.0 if output_normalized == expected_normalized else 0.0

    # Provide explanation
    if score == 1.0:
        observation = "Exact match found"
    else:
        observation = f"No match: expected '{output_true}' but got '{output}'"

    return score, observation
```

## Comprendre les Entrées Requises

Le paramètre `require` spécifie les entrées dont votre métrique a besoin. Les options courantes incluent :

- `output` : La réponse générée par le modèle
- `output_true` : La réponse attendue/de référence
- `query` : La question/prompt d'entrée
- `context` : Contexte supplémentaire fourni
- `retrieval_context` : Documents récupérés (pour les métriques RAG)
- `reasoning` : Raisonnement étape par étape

## Enregistrement de la Métrique

La métrique est automatiquement enregistrée lorsque le fichier est placé dans le répertoire `evalap/api/metrics/`. L'enregistrement se fait via le fichier `__init__.py` qui importe tous les fichiers Python du répertoire.

## Tester Votre Métrique

Créez des tests pour votre métrique :

```python
# tests/api/metrics/test_my_custom_metric.py

import pytest
from evalap.api.metrics import metric_registry

def test_my_custom_metric():
    metric_func = metric_registry.get_metric_function("my_custom_metric")

    # Test perfect match
    score, observation = metric_func(
        output="Paris is the capital of France",
        output_true="Paris is the capital of France",
        query="What is the capital of France?"
    )
    assert score == 1.0

    # Test partial match
    score, observation = metric_func(
        output="Paris",
        output_true="Paris is the capital of France",
        query="What is the capital of France?"
    )
    assert 0 < score < 1

    # Test no match
    score, observation = metric_func(
        output="London is the capital of UK",
        output_true="Paris is the capital of France",
        query="What is the capital of France?"
    )
    assert score == 0.0
```

## Utiliser Votre Métrique

Une fois enregistrée, votre métrique peut être utilisée dans des expériences :

```python
from evalap.api.metrics import metric_registry

# Get the metric function
metric_func = metric_registry.get_metric_function("my_custom_metric")

# Use it to evaluate
score, reason = metric_func(
    output="The model's answer",
    output_true="The expected answer",
    query="What is the question?"
)

print(f"Score: {score}")
print(f"Reason: {reason}")
```

## Sujets Avancés

### Intégrer des Métriques DeepEval

Evalap intègre automatiquement plusieurs métriques DeepEval. Pour ajouter une nouvelle métrique DeepEval :

1. Ajoutez le nom de la classe métrique à la liste `classes` dans `evalap/api/metrics/__init__.py`
2. Le système l'enregistrera automatiquement avec le nommage et les exigences appropriés

### Gérer Différents Types d'Entrées

Pour les métriques qui nécessitent des entrées différentes des entrées standard, vous pouvez les mapper en utilisant le `deepeval_require_map` :

```python
deepeval_require_map = {
    "input": "query",
    "actual_output": "output",
    "expected_output": "output_true",
    "context": "context",
    "retrieval_context": "retrieval_context",
    "reasoning": "reasoning",
}
```

### Gestion des Erreurs

Gérez toujours les erreurs potentielles avec élégance :

```python
try:
    score = float(answer)
except ValueError:
    score = None
    observation = "Failed to parse score from LLM response"
```

## Bonnes Pratiques

1. **Nommage Clair** : Utilisez des noms descriptifs qui indiquent ce que mesure la métrique
2. **Documentation** : Fournissez des descriptions claires dans le paramètre `description`
3. **Notation Cohérente** : Utilisez une échelle cohérente (généralement 0-1)
4. **Explications** : Retournez toujours des observations/raisons significatives avec les scores
5. **Validation des Entrées** : Validez les entrées requises avant le traitement
6. **Réglages de Température** : Pour les métriques LLM-as-judge, utilisez une température basse pour la cohérence

## Conclusion

En suivant ces étapes, vous pouvez ajouter des métriques personnalisées à Evalap qui s'intègrent parfaitement à la plateforme d'évaluation. Le système de registre de métriques facilite l'ajout de nouveaux critères d'évaluation tout en maintenant la cohérence à travers la plateforme.
