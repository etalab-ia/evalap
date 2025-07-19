---
sidebar_position: 1
---

# Installation avec Docker

Ce guide vous accompagnera dans le processus d'installation et d'exécution d'Evalap en utilisant Docker.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

- Docker version 18.0.6 ou supérieure.

## Exécuter avec compose

Créez un fichier `compose.yml` avec le contenu suivant :

```yaml
services:
  postgres:
    image: postgres:16.5
    restart: always
    user: postgres
    environment:
      - TZ=Europe/Paris
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres_password
      - POSTGRES_DB=evalap
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready", "-U", "postgres"]
      interval: 4s
      timeout: 10s
      retries: 5
      start_period: 60s

  evalap:
    image: ghcr.io/etalab-ia/evalap/evalap:main-latest
    restart: always
    environment:
      - TZ=Europe/Paris
      - ENV=prod
      - DB_NAME=${DB_NAME:-evalap}
      - POSTGRES_URL=${POSTGRES_URL:-postgresql://postgres:postgres_password@postgres:5432/evalap}
      - ADMIN_TOKEN=${ADMIN_TOKEN}
      - MFS_API_KEY_V2=${MFS_API_KEY_V2}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - ALBERT_API_KEY=${ALBERT_API_KEY}
    ports:
      - "8000:8000"
      - "8501:8501"
      - "3000:3000"
    volumes:
      - evalap_data:/data
    command: ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
    depends_on:
      postgres:
        condition: service_started

volumes:
  postgres_data:
  evalap_data:
```

Ensuite, exécutez l'application avec :

```bash
docker compose up -d
```

Cela démarrera à la fois l'application et les services de base de données en mode détaché.

Vous devriez alors pouvoir vous connecter aux services suivants :
- l'API à l'adresse http://localhost:8000/docs
- l'application web à l'adresse http://localhost:8501


## Prochaines étapes

Maintenant que vous avez installé Evalap avec Docker, vous pouvez :

- [Ajouter votre jeu de données](../user-guides/add-your-dataset.md) pour commencer à évaluer des modèles
- [Créer une expérience simple](../user-guides/create-a-simple-experiment.md) pour tester la plateforme
- Explorer les exemples de notebooks Jupyter dans le répertoire `notebooks/`
