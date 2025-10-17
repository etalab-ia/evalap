"""
Database seeding module for initializing datasets.

This module provides functionality to seed the database with predefined datasets
for development, testing, or initial setup purposes.
"""

import pandas as pd
from sqlalchemy.orm import Session

from evalap.api import crud, schemas
from evalap.api.db import SessionLocal, create_database_if_not_exists


def create_sample_qa_dataset(db: Session) -> None:
    """Create a sample Q&A dataset for testing."""
    data = {
        "question": [
            "What is the capital of France?",
            "Who wrote Romeo and Juliet?",
            "What is the largest planet in our solar system?",
            "What year did World War II end?",
            "What is the chemical symbol for gold?",
        ],
        "output_true": [
            "Paris",
            "William Shakespeare",
            "Jupiter",
            "1945",
            "Au",
        ],
        "context": [
            "France is a country in Western Europe.",
            "Shakespeare was an English playwright and poet.",
            "The solar system contains eight planets.",
            "World War II was a global conflict.",
            "Gold is a chemical element with atomic number 79.",
        ],
    }

    df = pd.DataFrame(data)

    dataset = schemas.DatasetCreate(
        name="sample_qa_dataset",
        readme="A sample Q&A dataset for testing basic question-answering capabilities.",
        default_metric="exact_match",
        columns_map={
            "question": "input",
            "output_true": "output_true",
            "context": "context",
        },
        df=df.to_json(),
    )

    # Check if dataset already exists
    existing = crud.get_dataset_by_name(db, dataset.name)
    if existing:
        print(f"Dataset '{dataset.name}' already exists (ID: {existing.id}). Skipping.")
        return

    created = crud.create_dataset(db, dataset)
    print(f"Created dataset: {created.name} (ID: {created.id})")


def create_math_dataset(db: Session) -> None:
    """Create a sample math problems dataset."""
    data = {
        "problem": [
            "What is 15 + 27?",
            "Calculate 8 × 9",
            "What is 100 - 37?",
            "Solve: 144 ÷ 12",
            "What is 5²?",
        ],
        "answer": [
            "42",
            "72",
            "63",
            "12",
            "25",
        ],
        "difficulty": [
            "easy",
            "easy",
            "easy",
            "medium",
            "medium",
        ],
    }

    df = pd.DataFrame(data)

    dataset = schemas.DatasetCreate(
        name="sample_math_dataset",
        readme="A sample dataset containing basic math problems for testing arithmetic capabilities.",
        default_metric="exact_match",
        columns_map={
            "problem": "input",
            "answer": "output_true",
        },
        df=df.to_json(),
    )

    # Check if dataset already exists
    existing = crud.get_dataset_by_name(db, dataset.name)
    if existing:
        print(f"Dataset '{dataset.name}' already exists (ID: {existing.id}). Skipping.")
        return

    created = crud.create_dataset(db, dataset)
    print(f"Created dataset: {created.name} (ID: {created.id})")


def create_sentiment_dataset(db: Session) -> None:
    """Create a sample sentiment analysis dataset."""
    data = {
        "text": [
            "I absolutely loved this movie! It was fantastic.",
            "This product is terrible and broke after one day.",
            "The service was okay, nothing special.",
            "Amazing experience, highly recommend!",
            "Worst purchase ever, complete waste of money.",
        ],
        "sentiment": [
            "positive",
            "negative",
            "neutral",
            "positive",
            "negative",
        ],
        "confidence": [
            0.95,
            0.92,
            0.78,
            0.96,
            0.94,
        ],
    }

    df = pd.DataFrame(data)

    dataset = schemas.DatasetCreate(
        name="sample_sentiment_dataset",
        readme="A sample dataset for sentiment analysis tasks with labeled text examples.",
        default_metric="exact_match",
        columns_map={
            "text": "input",
            "sentiment": "output_true",
        },
        df=df.to_json(),
    )

    # Check if dataset already exists
    existing = crud.get_dataset_by_name(db, dataset.name)
    if existing:
        print(f"Dataset '{dataset.name}' already exists (ID: {existing.id}). Skipping.")
        return

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

    create_sample_qa_dataset(db)
    create_math_dataset(db)
    create_sentiment_dataset(db)

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
