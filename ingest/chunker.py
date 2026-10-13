# ingest/chunker.py
# Splits parsed document text into overlapping chunks, each tagged with its source.

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, source: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
    """Split text into chunks and return a list of {text, source, chunk_id} records."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    pieces = splitter.split_text(text)
    return [
        {"text": piece, "source": source, "chunk_id": i}
        for i, piece in enumerate(pieces)
    ]


if __name__ == "__main__":
    # Test on every file in docs/:  python -m ingest.chunker
    import os
    from ingest.parsers import load_document

    for filename in os.listdir("docs"):
        path = os.path.join("docs", filename)
        try:
            text = load_document(path)
            chunks = chunk_text(text, source=filename)
            sizes = [len(c["text"]) for c in chunks]
            print(f"\n{'=' * 50}")
            print(f"FILE: {filename}")
            if not chunks:
                print("No chunks produced (file may be empty or unreadable)")
                continue
            print(f"Chunks: {len(chunks)}")
            print(f"Chunk length: min={min(sizes)}, max={max(sizes)}, avg={sum(sizes) // len(sizes)}")
            print(f"First chunk: {chunks[0]['text'][:150]!r}")
        except Exception as e:
            print(f"\n{'=' * 50}")
            print(f"FILE: {filename} - FAILED: {e}")