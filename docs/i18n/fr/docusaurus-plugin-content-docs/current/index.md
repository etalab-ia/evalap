---
id: intro
sidebar_position: 1
sidebar_label: Introduction
---

# Vue d'ensemble de la documentation

:::info
Actuellement, l'application web EvalAP (frontend) est une application en lecture seule permettant de visualiser les données d'évaluation.
Pour publier des jeux de données et exécuter des expériences, vous devez utiliser l'API EvalAP depuis votre propre instance si vous l'hébergez vous-même.
:::


<div className="container">
  <div className="row">
    <div className="col col--4">
      <div className="featureCard">
        <h3 className="featureTitle">Premiers pas</h3>
        <p className="featureDescription">Apprenez comment installer et configurer Evalap sur votre système.</p>
        <a href="docs/getting-started/install-from-source">Installer depuis les sources →</a><br/>
        <a href="docs/getting-started/install-with-docker">Installer avec Docker →</a>
      </div>
    </div>
    <div className="col col--4">
      <div className="featureCard">
        <h3 className="featureTitle">Guides d'utilisation</h3>
        <p className="featureDescription">Découvrez comment utiliser Evalap pour vos besoins d'évaluation.</p>
        <a href="docs/user-guides/add-your-dataset">Ajouter votre jeu de données →</a><br/>
        <a href="docs/user-guides/create-a-simple-experiment">Créer une expérience →</a>
      </div>
    </div>
    <div className="col col--4">
      <div className="featureCard">
        <h3 className="featureTitle">Guide du développeur</h3>
        <p className="featureDescription">Étendez et personnalisez Evalap selon vos besoins spécifiques.</p>
        <a href="docs/developer-guide/adding-a-new-metric">Ajouter une nouvelle métrique →</a><br/>
        <a href="docs/developer-guide/increase-parallel-requests">Augmenter les requêtes parallèles →</a>
      </div>
    </div>
  </div>
  <div className="row" style={{marginTop: '20px'}}>
    <div className="col col--4 col--offset-0">
      <div className="featureCard">
        <h3 className="featureTitle">Référence de l'API</h3>
        <p className="featureDescription">Spécification technique complète de l'API Evalap.</p>
        <span>Consultez la documentation de l'API sur <code>/docs</code> ou <code>/redoc</code> sur votre instance locale.</span>
      </div>
    </div>
  </div>
</div>

## Contribuer

Vous pouvez ouvrir des issues pour les bugs que vous avez trouvés ou les fonctionnalités qui vous semblent manquantes. Vous pouvez également soumettre des pull requests ou ouvrir des discussions sur le dépôt Evalap.

Pour commencer, consultez le fichier CONTRIBUTING.md dans [le dépôt](https://github.com/etalab-ia/evalap).
