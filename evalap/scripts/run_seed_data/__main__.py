"""
Database seeding module for initializing datasets.

This module provides functionality to seed the database with predefined datasets
for development, testing, or initial setup purposes.
"""

from datasets import load_dataset
from sqlalchemy.orm import Session

from evalap.api import crud, schemas
from evalap.api.db import SessionLocal, create_database_if_not_exists


def create_civics_dataset(db: Session) -> None:
    """Create the CIVICS dataset for evaluating cultural values in LLMs."""
    dataset_name = "llm-values-CIVICS"

    # Check if dataset already exists before downloading
    existing = crud.get_dataset_by_name(db, dataset_name)
    if existing:
        print(f"Dataset '{dataset_name}' already exists (ID: {existing.id}). Skipping.")
        return

    print("Loading CIVICS dataset from Hugging Face...")

    # Load the CIVICS dataset from Hugging Face
    ds = load_dataset("llm-values/CIVICS")

    # Convert to pandas DataFrame
    df_civics = ds["test"].to_pandas()

    dataset = schemas.DatasetCreate(
        name=dataset_name,
        readme=(
            "'Culturally-Informed & Values-Inclusive Corpus for Societal Impacts' is a dataset "
            "designed to evaluate the social and cultural variation of Large Language Models (LLMs) "
            "towards socially sensitive topics across multiple languages and cultures."
        ),
        df=df_civics.to_json(),
        default_metric="bias",
        columns_map={"query": "Statement"},
        compliance=True,
    )

    created = crud.create_dataset(db, dataset)
    print(f"Created dataset: {created.name} (ID: {created.id})")


def create_toxic_chat_dataset(db: Session) -> None:
    """Create the lmsys-toxic-chat dataset for toxicity detection."""
    dataset_name = "lmsys-toxic-chat"

    # Check if dataset already exists before downloading
    existing = crud.get_dataset_by_name(db, dataset_name)
    if existing:
        print(f"Dataset '{dataset_name}' already exists (ID: {existing.id}). Skipping.")
        return

    print("Loading lmsys-toxic-chat dataset from Hugging Face...")

    # Load the toxic-chat dataset from Hugging Face
    ds = load_dataset("lmsys/toxic-chat", "toxicchat0124")

    # Convert to pandas DataFrame
    df_toxic_chat = ds["test"].to_pandas()

    dataset = schemas.DatasetCreate(
        name=dataset_name,
        readme=(
            "This dataset contains toxicity annotations on 10K user prompts "
            "collected from the Vicuna online demo."
        ),
        df=df_toxic_chat.to_json(),
        default_metric="toxicity",
        columns_map={"query": "user_input"},
        compliance=True,
    )

    created = crud.create_dataset(db, dataset)
    print(f"Created dataset: {created.name} (ID: {created.id})")


def create_deccp_dataset(db: Session) -> None:
    """Create the DECCP dataset for Chinese censorship benchmarking."""
    dataset_name = "DECCP"

    # Check if dataset already exists before downloading
    existing = crud.get_dataset_by_name(db, dataset_name)
    if existing:
        print(f"Dataset '{dataset_name}' already exists (ID: {existing.id}). Skipping.")
        return

    print("Loading DECCP dataset from Hugging Face...")

    # Load the DECCP dataset from Hugging Face
    ds = load_dataset("augmxnt/deccp")

    # Convert to pandas DataFrame (using censored split)
    df_censored = ds["censored"].to_pandas()

    dataset = schemas.DatasetCreate(
        name=dataset_name,
        readme="Chineses Censorship Benchmark from https://huggingface.co/datasets/augmxnt/deccp",
        df=df_censored.to_json(),
        default_metric="answer_relevancy",
        columns_map={"query": "text"},
        compliance=True,
    )

    created = crud.create_dataset(db, dataset)
    print(f"Created dataset: {created.name} (ID: {created.id})")


def create_service_public_dataset(db: Session) -> None:
    """Create dataset test_service_public to evaluate responses regarding French public services."""
    dataset_name = "test_service_public"

    # Check if dataset already exists before downloading
    existing = crud.get_dataset_by_name(db, dataset_name)
    if existing:
        print(f"Dataset '{dataset_name}'  already exists  (ID: {existing.id}). Skipping.")
        return

    print("Add dataset test_service_public...")

    import pandas as pd

    query = [
        "Comment changer le titulaire sur la carte grise suite au décès du conjoint ?",
        "Combien faut-il de trimestres cotisés pour une retraite à taux plein ?",
        "Quelle est la démarche pour demander son casier judiciaire ?",
        "comment fonctionne la taxe foncière dans le cadre d’une location ?",
    ]

    output_true = [
        """La carte grise pourra être mise au nom de l'époux survivant.

    Vous devez effectuer la démarche en ligne en utilisant via téléservice de l'ANTS (Agence Nationale des titres sécurisés).

    Vous devez vous munir d'une copie numérique (photo ou scan) des documents suivants :
    - Formulaire cerfa n°13750
    - Justificatif de domicile de moins de 6 mois
    - Carte grise originale
    - Pièce d'identité en cours de validité
    - Livret de famille attestant du décès, du régime matrimonial et du nombre de co-héritiers
    - Mandat signé et pièce d'identité de la personne pour qui vous effectuez la démarche

    Vous devez certifier sur l'honneur que le demandeur du certificat d’immatriculation a une attestation d'assurance du véhicule et un permis de conduire correspondant à la catégorie du véhicule immatriculé.

    Vous n'avez pas à joindre une copie numérique (photo ou scan) du permis de conduire. Mais celle-ci pourra vous être demandée lors de l'instruction de votre dossier.

    La preuve d'un contrôle technique en cours de validité est demandée si le véhicule le nécessite. Elle peut être apportée par la vignette de contrôle technique apposée sur la carte grise.

    Le règlement du montant du certificat d’immatriculation doit obligatoirement être effectué par carte bancaire.

    À la fin de la procédure, vous obtenez les 3 éléments suivants :
    - Numéro de dossier
    - Accusé d'enregistrement de votre demande
    - Certificat provisoire d'immatriculation (CPI), que vous devez imprimer.
    Le CPI vous permet de circuler pendant 1 mois, uniquement en France, en attendant de recevoir votre certificat d'immatriculation définitif.
    Vous pourrez suivre sur internet l'état d'avancement de sa fabrication.""",
        """En France, pour bénéficier d’une retraite à taux plein (sans décote), il faut généralement avoir cotisé un certain nombre de trimestres, qui dépend de votre année de naissance.
    Voici les règles actuelles (2025) :
    - Pour les assurés nés en 1965 ou après, il faut 172 trimestres (soit 43 ans de cotisation).
    - Pour les assurés nés avant 1965, le nombre de trimestres requis est progressivement augmenté selon l’année de naissance.
    Exemple :
    - Nés en 1960 : 167 trimestres
    - Nés en 1961 : 168 trimestres
    - Nés en 1962 : 169 trimestres
    - Nés en 1963 : 170 trimestres
    - Nés en 1964 : 171 trimestres""",
        """La procédure pour demander votre casier judiciaire varie en fonction de votre lieu de naissance. En France, pour demander une copie de votre casier judiciaire (bulletin n°3), voici la démarche à suivre en 2025 :

    1. En ligne (recommandé)
    Site officiel : Rendez-vous sur le site service-public.fr ou directement sur casier-judiciaire.justice.gouv.fr.
    Créer un compte : Vous devez vous connecter via FranceConnect (avec vos identifiants impots.gouv.fr, Ameli, La Poste, etc.).
    Formulaire : Remplissez le formulaire en ligne, vérifiez vos informations d’état civil et validez votre demande.
    Réception : Le bulletin n°3 vous est envoyé par email sous 24 à 48 heures (gratuit).

    2. Par courrier
    - Formulaire : Téléchargez et imprimez le formulaire Cerfa n°14881*02 depuis service-public.fr.
    - Pièces à joindre : Copie recto-verso de votre pièce d’identité (CNI, passeport, titre de séjour).
    - Envoi : Envoyez le tout à l’adresse suivante : Ministère de la Justice - Casier judiciaire national 107 rue du Landreau 44317 Nantes Cedex 3
    Réception : Sous 10 à 15 jours (gratuit).

    3. Sur place
    - Tribunal judiciaire : Vous pouvez vous rendre au greffe du tribunal judiciaire de votre domicile, muni d’une pièce d’identité.
    - Réception : Le bulletin n°3 vous est remis immédiatement (gratuit).

    À savoir
    - Le bulletin n°3 est gratuit et personnel.
    - Il ne contient que les condamnations non effacées par la réhabilitation ou l’amnistie.
    - Pour les ressortissants étrangers, la démarche est similaire, mais il faut fournir un justificatif de domicile en France.""",
        """En France, la taxe foncière est un impôt local qui s’applique aux propriétaires de biens immobiliers. Voici comment elle fonctionne dans le cadre d’une location :
    - Le propriétaire (bailleur) est redevable de la taxe foncière, même si le logement est loué.
    - Le locataire n’est pas responsable du paiement, sauf si le bail prévoit explicitement un remboursement au propriétaire (ce qui est rare et doit être clairement stipulé).

    La loi interdit généralement au propriétaire de facturer la taxe foncière au locataire, sauf si le bail le prévoit (par exemple, pour les locations meublées ou certains baux commerciaux).

    Elle finance les services locaux (écoles, voirie, etc.) et est calculée sur la valeur locative cadastrale du bien.""",
    ]

    df = pd.DataFrame({"query": query, "output_true": output_true})

    dataset = schemas.DatasetCreate(
        name=dataset_name,
        readme=(
            "Test dataset for answers to frequently asked questions about administrative procedures and public services in France. Useful for launching a quick evaluation campaign and understanding how EvalAP works."
        ),
        df=df.to_json(),
        default_metric="judge_notator",
        compliance=False,
    )

    created = crud.create_dataset(db, dataset)
    print(f"Created dataset: {created.name} (ID: {created.id})")


def create_annuaire_entreprises_dataset(db: Session) -> None:
    """Add le dataset test_annuaire_entreprises to evaluate answers about administrative acronyms."""
    dataset_name = "test_annuaire_entreprises"

    # Check if dataset already exists before downloading
    existing = crud.get_dataset_by_name(db, dataset_name)
    if existing:
        print(f"Dataset '{dataset_name}'  already exists (ID: {existing.id}). Skipping.")
        return

    print("Add dataset test_annuaire_entreprises...")

    import pandas as pd

    query = ["Qu'est ce que la DGCCRF", "Qu'est ce que la DINUM"]
    output_true = [
        """L’administration DIRECTION GENERALE DE LA CONCURRENCE, DE LA CONSOMMATION ET DE LA REPRESSION DES FRAUDES (DGCCRF) a été créée le 5 novembre 1985, il y a 40 ans. Sa forme juridique est Service central d'un ministère.
    Son domaine d’activité est : administration publique (tutelle) des activités économiques. En 2023, elle était catégorisée Entreprise de Taille Intermédiaire. Elle possédait 500 à 999 salariés.

    La DGCCRF est une administration française qui dépend du ministère de l’Économie. Ses missions principales sont :
    - Protéger les consommateurs : veille au respect des droits des consommateurs, lutte contre les pratiques commerciales trompeuses, arnaques, et produits dangereux.
    - Garantir la loyauté des marchés : surveillance des pratiques anticoncurrentielles, ententes illicites entre entreprises, et abus de position dominante.
    - Contrôler la qualité et la sécurité des produits : contrôles sur les produits et services mis sur le marché pour conformité aux normes.
    - Réprimer les fraudes : sanctions possibles des entreprises ne respectant pas la réglementation, en collaboration avec la justice.
    En résumé, la DGCCRF agit pour que les marchés fonctionnent équitablement et que les consommateurs soient protégés.""",
        """La Direction interministérielle du numérique (DINUM) accompagne les ministères dans leur transformation numérique, conseille le gouvernement et développe des services et ressources partagées comme le réseau interministériel de l’État, FranceConnect, data.gouv.fr ou api.gouv.fr. Elle pilote, avec l’appui des ministères, le programme Tech.gouv d’accélération de la transformation numérique du service public. Créée par décret le 25 octobre 2019, la DINUM a pris la suite de la DINSIC.

    Quelques responsables importants :
    - Directrice : Stéphanie SCHAER
    - Adjoint à la directrice : Jérémie VALLET
    - Responsable communication : Floriane BEAUDRON
    - Responsable juridique : Perica SUCEVIC
    - Responsable pilotage des ressources financières : Arnaud GODDAT
    - Administratrice générale des données déléguée : Cécile LE GUEN
    - Responsable sécurité des systèmes d'information : Frédéric CULIE""",
    ]

    df = pd.DataFrame({"query": query, "output_true": output_true})

    dataset = schemas.DatasetCreate(
        name=dataset_name,
        readme=(
            "Test dataset for answers to questions about administrative acronyms. Useful for launching a quick evaluation campaign and understanding how EvalAP works."
        ),
        df=df.to_json(),
        default_metric="judge_notator",
        compliance=False,
    )

    created = crud.create_dataset(db, dataset)
    print(f"Created dataset: {created.name} (ID: {created.id})")


def seed_all_datasets(db: Session | None = None) -> None:
    """
    Seed all predefined datasets into the database.

    Args:
        db: Optional database session. If not provided, a new session will be created.
    """
    if db is None:
        db = SessionLocal()
        try:
            _seed_with_session(db)
        finally:
            db.close()
    else:
        _seed_with_session(db)


def _seed_with_session(db: Session) -> None:
    """Internal function to seed datasets with a given session."""
    print("Starting database seeding...")
    print("-" * 50)

    try:
        create_civics_dataset(db)
    except Exception as e:
        print(f'Error creating civics dataset: {e}')

    try:
        create_toxic_chat_dataset(db)
    except Exception as e:
        print(f'Error creating toxic chat dataset: {e}')

    try:
        create_deccp_dataset(db)
    except Exception as e:
        print(f'Error creating deccp dataset: {e}')

    try:
        create_service_public_dataset(db)
    except Exception as e:
        print(f'Error creating service public dataset: {e}')

    try:
        create_annuaire_entreprises_dataset(db)
    except Exception as e:
        print(f'Error creating annuaire entreprises dataset: {e}')

    print("-" * 50)
    print("Database seeding completed!")


def main():
    """Main entry point for running the seed script."""
    # Ensure database exists
    create_database_if_not_exists()

    # Seed the database
    seed_all_datasets()


if __name__ == "__main__":
    main()
