---
sidebar_position: 4
---

# Générer les réponses localement avec vLLM

Ce guide vous accompagne dans le processus de génération de réponses de modèles localement en utilisant des machines équipées de GPU, puis de soumission d'expériences à Evalap.
Nous fournissons deux scripts utilitaires pour vous aider à accomplir cela :
- `run_answers.py` : Générer des réponses de modèle pour un jeu de données Evalap
- `run_expe.py` : Créer ou mettre à jour des ensembles d'expériences dans Evalap

## Prérequis

- Accès à une machine avec capacités GPU
- Accès SSH configuré avec votre clé publique (si nécessaire)
- Environnement Python avec support des environnements virtuels
- Espace disque suffisant pour les téléchargements de modèles
- [vLLM](https://docs.vllm.ai/) installé

## Étape 1 : Se connecter à la machine GPU (si nécessaire)

Connectez-vous à votre VM ou machine équipée de GPU en utilisant SSH :

```bash
# Add your SSH key to the agent
ssh-add ~/.ssh/your_key

# Connect to the machine
ssh user@gpu-machine-address
```

## Étape 2 : Vérifier l'espace disque disponible

Avant de télécharger des modèles, assurez-vous d'avoir suffisamment d'espace disque :

```bash
# Check disk usage
df -Th

# If needed, clean up old model cache
# Models are stored in ~/.cache/huggingface/hub/ by default
rm -rf ~/.cache/huggingface/hub/old_models/
```

⚠️ **Note** : Les grands modèles de langage peuvent nécessiter un espace disque important (10-100 Go par modèle). Planifiez en conséquence.

## Étape 3 : Lancer le modèle avec vLLM

Démarrez le serveur de modèle en utilisant vLLM. Voici un exemple avec Gemma-3 :

```bash
vllm serve google/gemma-3-27b-it \
  --gpu-memory-utilization 1 \
  --tensor-parallel-size 1 \
  --max-model-len 32768 \
  --port 9191
```

### Paramètres vLLM courants :
- `--gpu-memory-utilization` : Fraction de la mémoire GPU à utiliser (0-1)
- `--tensor-parallel-size` : Nombre de GPU pour le parallélisme de tenseurs
- `--max-model-len` : Longueur maximale de séquence
- `--port` : Port pour le serveur API

## Étape 4 : Installer le framework Evalap

Clonez et installez le dépôt Evalap :

```bash
# Clone the repository
git clone https://github.com/etalab/evalap.git
cd evalap

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ./
```

Cette installation donne accès aux outils en ligne de commande situés dans le répertoire `evalap/scripts/`.

## Étape 5 : Générer des réponses

Utilisez le script `run_answers.py` pour générer des réponses depuis votre modèle :

```bash
# Set your API keys
export EVALAP_API_KEY="your-evalap-token"
export OPENAI_API_KEY="your-openai-key"  # Optional, if not using --auth-token

# View available options
python -m evalap.scripts.run_answers.run_answers --help

# Example: Generate answers for MFS questions with Gemma-3
python -m evalap.scripts.run_answers.run_answers \
  --run-name gemma-3-27b_mfs \
  --base-url http://localhost:9191/v1 \
  --model google/gemma-3-27b-it \
  --dataset MFS_questions_v01 \
  --repeat 4 \
  --max-workers 8
```

### Paramètres clés :
- `--run-name` : Identifiant unique pour cette exécution de génération
- `--base-url` : URL du serveur vLLM (ex : http://localhost:9191/v1)
- `--model` : Nom/identifiant du modèle
- `--dataset` : Nom du jeu de données Evalap à utiliser
- `--repeat` : Nombre de fois à exécuter le jeu de données (par défaut : 1)
- `--max-workers` : Nombre maximum de requêtes concurrentes (par défaut : 8)
- `--system-prompt` : Prompt système optionnel à ajouter aux requêtes
- `--sampling-params` : Chaîne JSON optionnelle avec les paramètres d'échantillonnage (ex : `'{"temperature": 0.7, "max_tokens": 1024}'`)

Le script va :
1. Télécharger le jeu de données spécifié depuis Evalap
2. Générer des réponses pour chaque requête dans le jeu de données
3. Sauvegarder les résultats dans `results/{run_name}__{repetition}.json`
4. Sauvegarder les détails du modèle dans `results/{run_name}__details.json`

## Étape 6 : Créer et exécuter des expériences

Utilisez `run_expe.py` pour créer des ensembles d'expériences et les soumettre à Evalap :

```bash
# View available options
python -m evalap.scripts.run_expe.run_expe --help

# Create a new experiment
python -m evalap.scripts.run_expe.run_expe \
  --run-name gemma-3-27b_mfs \
  --expe-name "Gemma-3 27B MFS Evaluation"

# Update an existing experiment set
python -m evalap.scripts.run_expe.run_expe \
  --run-name gemma-3-27b_mfs \
  --expset existing-experiment-id
```

### Paramètres clés :
- `--run-name` : Nom de la génération de modèle à charger (doit correspondre aux fichiers dans le répertoire `results/`)
- `--expe-name` : Nom d'affichage pour l'ensemble d'expériences (optionnel, par défaut : run-name)
- `--expset` : ID de l'ensemble d'expériences existant à mettre à jour (optionnel)

Le script va :
1. Charger tous les fichiers de résultats correspondant à `results/{run_name}*.json`
2. Créer un ensemble d'expériences avec les métriques : answer_relevancy, judge_exactness, judge_notator, output_length, generation_time
3. Soumettre l'ensemble d'expériences à Evalap pour évaluation

## Exemple de flux de travail complet

```bash
# 1. Start vLLM server
vllm serve google/gemma-3-27b-it --gpu-memory-utilization 0.9 --port 9191

# 2. Generate answers (in another terminal)
python -m evalap.scripts.run_answers.run_answers \
  --run-name gemma3_test \
  --base-url http://localhost:9191/v1 \
  --model google/gemma-3-27b-it \
  --dataset MFS_questions_v01 \
  --repeat 3

# 3. Submit experiment to Evalap
python -m evalap.scripts.run_expe.run_expe \
  --run-name gemma3_test \
  --expe-name "Gemma-3 Test Run"
```

## Bonnes pratiques

1. **Gestion des ressources** : Surveillez l'utilisation de la mémoire GPU et ajustez `--gpu-memory-utilization` en conséquence
2. **Requêtes concurrentes** : Ajustez `--max-workers` en fonction de la capacité de votre modèle et de la taille du jeu de données
3. **Suivi des expériences** : Utilisez des noms d'expériences significatifs et maintenez des métadonnées pour la reproductibilité
4. **Exécutions multiples** : Utilisez `--repeat` pour générer plusieurs exécutions pour la signification statistique
5. **Clés API** : Stockez vos clés API dans des variables d'environnement pour la sécurité

## Dépannage

### Problèmes courants :

**Erreur de mémoire insuffisante**
```bash
# Reduce memory utilization
--gpu-memory-utilization 0.8
```

**Connexion refusée**
```bash
# Check if vLLM server is running
curl http://localhost:9191/v1/models
```

**Génération lente**
```bash
# Adjust batch size and parallelism
--tensor-parallel-size 2  # If multiple GPUs available
```

**Fichiers de résultats manquants**
```bash
# Check that result files were generated
ls results/{run_name}*.json
```

**Problèmes d'authentification API**
```bash
# Ensure API keys are set
echo $EVALAP_API_KEY
echo $OPENAI_API_KEY
```
