import hashlib
import re
from pathlib import Path


def chunk_document(document: str, max_words: int, tolerance: float = 2.1) -> list[dict]:
    """
    Split documents into coherent chunks based on paragraphs.

    Args:
        documents: List of document texts
        max_words: Maximum number of words per chunk
        tolerance: ratio of words to allow exceeding max_words by

    Returns:
        List of dictionaries containing 'id' and 'text' keys
    """
    chunks = []

    # Split on double newlines to get paragraphs
    paragraphs = document.strip().split("\n\n")
    if len(paragraphs) == 1:
        paragraphs = document.strip().split("\n")

    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Clean
    # - If a paragraph is less than 10 words or contains no alphabetic char, merge it to the next one.
    for i, paragraph in enumerate(paragraphs):
        if len(paragraph.split()) < 5 or not re.search(r"[a-zA-Z]", paragraph):
            if i + 1 < len(paragraphs) and paragraphs[i + 1]:
                paragraphs[i + 1] = paragraph + "\n\n" + paragraphs[i + 1]
                paragraphs[i] = ""

    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Split again paragraphs based on "\n" if the size of paragraph exceed the tolerance ratio
    new_paragraphs = []
    for paragraph in paragraphs:
        if len(paragraph.split()) > max_words * tolerance:
            sub_paragraphs = paragraph.split("\n")
            sub_paragraphs = [p.strip() for p in sub_paragraphs if p.strip()]
            new_paragraphs.extend(sub_paragraphs)
        else:
            new_paragraphs.append(paragraph)
    paragraphs = new_paragraphs

    current_chunk = []
    current_word_count = 0

    for paragraph in paragraphs:
        # Count words in this paragraph
        paragraph_words = len(paragraph.split())

        # If adding this paragraph exceeds max_words and we have content, save current chunk
        if current_word_count + paragraph_words > max_words and current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunk_id = hashlib.sha256(chunk_text.encode()).hexdigest()
            chunks.append({"_id": chunk_id, "text": chunk_text})

            # Start new chunk with current paragraph
            current_chunk = [paragraph]
            current_word_count = paragraph_words
        else:
            # Add paragraph to current chunk
            current_chunk.append(paragraph)
            current_word_count += paragraph_words

    # Don't forget the last chunk
    if current_chunk:
        chunk_text = "\n\n".join(current_chunk)
        chunk_id = hashlib.sha256(chunk_text.encode()).hexdigest()
        chunks.append({"_id": chunk_id, "text": chunk_text})

    return chunks


def load_legalbenchrag(max_words=300) -> list[dict]:
    # Get all text files
    files = Path("notebooks/_data/LegalBenchRAG/corpus").glob("**/*.txt")
    files = sorted(files)

    # Load and chunk documents
    documents = []
    for file in files:
        with open(file, encoding="utf-8") as f:
            data = f.read()
        documents.extend(chunk_document(data, max_words=max_words))

    return documents
