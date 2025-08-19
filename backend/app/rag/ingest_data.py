
import argparse
import csv
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from retriever import get_index

load_dotenv()


def read_csv(input_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"CSV file not found: {input_path}")

    records: List[Dict[str, Any]] = []
    with open(input_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            # Some CSVs may include an unnamed index column with an empty header
            raw_id = (row.get("") or row.get(None) or "").strip() if isinstance(row, dict) else ""
            rid = raw_id if raw_id else str(i + 1)

            title = (row.get("Title") or "").strip()
            desc = (row.get("Desc") or "").strip()

            metadata: Dict[str, Any] = {
                "title": title,
                "description": desc,
                "type": (row.get("Type") or "").strip(),
                "body_part": (row.get("BodyPart") or "").strip(),
                "equipment": (row.get("Equipment") or "").strip(),
                "level": (row.get("Level") or "").strip(),
                "rating": (row.get("Rating") or "").strip(),
                "rating_desc": (row.get("RatingDesc") or "").strip(),
            }

            record: Dict[str, Any] = {
                "id": rid,
                "Title": title,
                "Desc": desc,
                "metadata": metadata,
            }

            records.append(record)

    return records


def build_text(record: Dict[str, Any]) -> str:
    # Prefer CSV fields
    title = (record.get("Title") or "").strip()
    desc = (record.get("Desc") or "").strip()
    if title or desc:
        return f"{title}\n\n{desc}".strip()

    # Fallback to legacy JSON fields if present
    prompt = record.get("prompt", "") or ""
    question = record.get("question", "") or ""
    if prompt and question and prompt != question:
        return f"{prompt}\n\n{question}"
    return (prompt or question).strip()


def embed_texts(texts: List[str]) -> List[List[float]]:
    embedder = OpenAIEmbeddings()
    return embedder.embed_documents(texts)


def upsert_records(records: List[Dict[str, Any]], namespace: str | None = None, batch_size: int = 100) -> None:
    index = get_index()

    texts: List[str] = [build_text(r) for r in records]
    vectors = embed_texts(texts)

    items: List[tuple[str, List[float], Dict[str, Any]]] = []
    for i, (record, vec, text) in enumerate(zip(records, vectors, texts)):
        rid = str(record.get("id") or i + 1)
        meta: Dict[str, Any] = {
            "text": text,
            "question": (record.get("Title") or record.get("question") or text) or "",
            "code": record.get("code", ""),
        }

        extra = record.get("metadata")
        if isinstance(extra, dict):

            for k, v in extra.items():
                if k not in meta:
                    meta[k] = v


        sanitized: Dict[str, Any] = {}
        for k, v in meta.items():
            if v is None:
                continue
            if isinstance(v, (str, int, float, bool)):
                sanitized[k] = v
            elif isinstance(v, list):
                # Convert list items to strings and drop empties
                str_list = [str(item).strip() for item in v if item is not None and str(item).strip()]
                sanitized[k] = str_list
            else:
                # Fallback: store string representation
                sanitized[k] = str(v)

        meta = sanitized

        items.append((rid, vec, meta))

    # Upsert in batches
    for start in range(0, len(items), batch_size):
        batch = items[start : start + batch_size]
        ids = [i for i, _, _ in batch]
        vecs = [v for _, v, _ in batch]
        metas = [m for _, _, m in batch]

        payload = list(zip(ids, vecs, metas))
        if namespace:
            index.upsert(vectors=payload, namespace=namespace)
        else:
            index.upsert(vectors=payload)

        print(f"Upserted {len(payload)} vectors ({start + len(payload)}/{len(items)})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest CSV records into Pinecone with exercise metadata")
    parser.add_argument(
        "--input",
        default=os.path.join(os.path.dirname(__file__), "megaGymDataset.csv"),
        help="Path to input CSV file",
    )
    parser.add_argument(
        "--namespace",
        default=None,
        help="Optional Pinecone namespace",
    )
    args = parser.parse_args()

    records = read_csv(args.input)
    if not records:
        print("No records to ingest.")
        return

    upsert_records(records, namespace=args.namespace)
    print("Done.")


if __name__ == "__main__":
    main()

