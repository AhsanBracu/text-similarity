from pathlib import Path


def read_text(file_path: Path) -> str:
    raw = file_path.read_bytes()

    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        # Some files are Windows-1252 (e.g. byte 0x85 = "…")
        return raw.decode("cp1252", errors="replace")


def load_documents(folder_path: str, limit: int = 10) -> dict[str, str]:
    documents = {}

    for file_path in sorted(Path(folder_path).glob("*.txt")):
        content = read_text(file_path)

        for line in content.split("\n"):
            parts = line.strip().split("|", maxsplit=2)

            if len(parts) != 3:
                continue

            tweet_id, date, text = parts

            if text.strip():
                documents[tweet_id] = text.strip()

            if len(documents) >= limit:
                return documents

    return documents
