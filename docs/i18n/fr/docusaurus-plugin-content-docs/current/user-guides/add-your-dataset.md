---
sidebar_position: 1
---

# Publier un jeu de données

Ce guide vous accompagnera dans le processus d'ajout d'un nouveau jeu de données à Evalap pour l'évaluation de modèles.
Vous pouvez ajouter un jeu de données par programmation en utilisant l'API Evalap.

Deux formats sont pris en charge : 

- Données de type CSV (dataframes)
- Format Parquet (pour les jeux de données plus volumineux)


## Mappage des colonnes


Evalap utilise une convention de nommage standard pour les colonnes. Lors de l'ajout de votre jeu de données, vous devez soit nommer vos colonnes en conséquence, soit mapper les colonnes de votre jeu de données à ces noms standards en utilisant le paramètre `columns_map` :

- `query`: (str) la requête d'entrée.
- `output`: (str) la réponse du modèle.
- `output_true`: (str) la réponse de référence.
- `context`: list[str] une liste d'informations contextuelles transmises au prompt.
- `retrieval_context`: list[str] une liste d'informations récupérées transmises au prompt.
- `reasoning`: (str) Les tokens de raisonnement associés à une réponse.
- (à venir) `tools_called`
- (à venir) `expected_tools`


Si les noms de colonnes de votre jeu de données ne correspondent pas à ces conventions, vous pouvez soit les renommer avant d'ajouter le jeu de données, soit utiliser le paramètre `columns_map` dans la requête pour fournir un mappage entre les noms de convention Evalap et les vôtres.



Par exemple, si votre jeu de données a des colonnes nommées "question" et "answer", vous les mappez comme ceci :

```json
"columns_map": {"input": "question", "output": "answer"}
```

Consultez la [référence de l'API](https://evalap.etalab.gouv.fr/redoc#tag/datasets/operation/create_dataset_v1_dataset_post) pour plus de détails d'utilisation.


## À partir d'un jeu de données de type CSV

Le code suivant montre comment télécharger un jeu de données vers Evalap à partir d'un fichier CSV.

```python
import requests
import json
import pandas as pd

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token (or None if launch locally)
HEADERS = {
    "Authorization": "Bearer YOUR_EVALAP_KEY",
    "Content-Type": "application/json"
}

# Load the dataset from a CSV file
dataset_df = pd.read_csv("my_dataset.csv")  # Pandas use "," as default limiter.


# Prepare dataset metadata
dataset = {
    "name": "My domain specific dataset",
    "readme": "A dataset for evaluating question answering capabilities",
    "default_metric": "judge_precision",
    "df": dataset_df.to_json()
}

# Create the dataset
response = requests.post( f"{API_URL}/datasets", headers=HEADERS, json=dataset)

dataset_id = response.json()["id"]

print(f"Dataset created with ID: {dataset_id}")
```


## À partir d'un jeu de données Parquet

Consultez le tutoriel de démonstration pour ajouter un jeu de données OCR fourni par la bibliothèque Marker : [create_marker_dataset.ipynb](https://github.com/etalab-ia/evalap/blob/main/notebooks/create_marker_dataset.ipynb)


## Prochaines étapes

Après avoir ajouté votre jeu de données, vous pouvez :

- [Créer une expérience simple](./create-a-simple-experiment.md) en utilisant votre jeu de données
- Explorer les jeux de données existants sur la plateforme
