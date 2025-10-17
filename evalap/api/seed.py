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

    create_civics_dataset(db)
    create_toxic_chat_dataset(db)

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
