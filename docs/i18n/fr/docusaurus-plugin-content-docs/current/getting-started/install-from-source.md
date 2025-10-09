---
sidebar_position: 2
---

# Installation depuis les sources

Ce guide vous accompagnera dans le processus d'installation d'Evalap à partir du code source. L'installation depuis les sources est recommandée pour les développeurs qui souhaitent contribuer au projet ou qui ont besoin des dernières fonctionnalités qui pourraient ne pas être disponibles dans les versions publiées.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

## Cloner le dépôt

```bash
git clone https://github.com/etalab-ia/evalap.git
cd evalap
```

## Créer un environnement virtuel (Recommandé)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

## Installer les dépendances

```bash
pip install .
```

## Configurer l'application

Pour protéger les requêtes API sensibles comme la suppression d'expériences ou de jeux de données, vous pouvez définir un jeton administrateur

```bash
export ADMIN_TOKEN="Your evalap admin token"
```

Vous pouvez accéder aux modèles LLM des principaux fournisseurs en configurant vos clés API si vous avez des comptes chez :

```bash
export OPENAI_API_KEY="Your secret key"
export ANTHROPIC_API_KEY="Your secret key"
export MISTRAL_API_KEY="Your secret key"
export ALBERT_API_KEY="Your secret key"
```

Vous pouvez également définir des variables d'environnement dans un fichier `.env` à la racine du projet.

Tous les paramètres globaux du projet et les variables d'environnement sont gérés dans `evalap/api/config.py`.

## Initialisation de la base de données

1. Lancez les services de développement :

```bash
docker compose -f compose.dev.yml up postgres
```

2. Créez le premier script de migration :

```bash
alembic -c evalap/api/alembic.ini revision --autogenerate -m "Table Initialization"
```

3. Initialisez/Mettez à jour le schéma de la base de données :

```bash
alembic -c evalap/api/alembic.ini upgrade head
```


## Exécuter l'application

```bash
# Step 1: Run the API server
uvicorn evalap.api.main:app --reload --host 0.0.0.0 --port 8000

# Step 2: In a separate terminal, activate your virtual environment if needed, then run the runner
PYTHONPATH="." python -m evalap.runners
```

### Vérifier l'installation

Pour vérifier qu'Evalap fonctionne correctement, ouvrez votre navigateur web et accédez à :

```
http://localhost:8000/redoc
```

Vous devriez voir la page de documentation de l'API. Vous pouvez également utiliser `http://localhost:8000/docs` si vous préférez la version swagger.

### Configuration des journaux

Vous pouvez ajuster le niveau de journalisation pour obtenir des informations plus détaillées :

```bash
# Run with debug logging enabled
LOG_LEVEL="DEBUG" PYTHONPATH="." python -m evalap.runners
```

### Résolution des problèmes

Si vous rencontrez des problèmes au démarrage de l'application :

1. Assurez-vous que toutes les dépendances sont correctement installées
2. Vérifiez que la base de données est en cours d'exécution (vérifiez les conteneurs Docker)
3. Vérifiez que les variables d'environnement sont correctement définies
4. Recherchez les messages d'erreur dans la sortie du terminal

L'API devrait maintenant fonctionner à l'adresse `http://localhost:8000`.

## Exécuter l'interface Streamlit (Optionnel)

```bash
streamlit run evalap/ui/demo_streamlit/app.py --server.runOnSave true
```


## Prochaines étapes

Maintenant que vous avez installé Evalap, vous pouvez :

- [Ajouter votre jeu de données](../user-guides/add-your-dataset.md) pour commencer à évaluer des modèles
- [Créer une expérience simple](../user-guides/create-a-simple-experiment.md) pour tester la plateforme
- Explorer les exemples de notebooks Jupyter dans le répertoire `notebooks/`
