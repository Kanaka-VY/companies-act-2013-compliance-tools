from typing import List

import chromadb
from sentence_transformers import SentenceTransformer


class ChromaService:
    def __init__(self, persist_dir: str, collection_name: str, embedding_model: str):
        self._embedder = SentenceTransformer(embedding_model)
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(name=collection_name)
        self._seed_if_empty()

    def _seed_if_empty(self) -> None:
        if self._collection.count() > 0:
            return
        docs = [
            "Always include clear, actionable recommendations with priority.",
            "Compliance records should be concise, factual, and auditable.",
            "Risk level should be derived from impact and likelihood.",
            "Use plain business language suitable for non-technical stakeholders.",
            "Every report should include summary, overview, and key items.",
            "Priorities map as High for urgent, Medium for planned, Low for monitoring.",
            "Recommendations should use verbs: implement, review, monitor, automate.",
            "Generated descriptions should avoid speculative legal statements.",
            "Escalate unresolved critical gaps within 24 hours.",
            "Track generated time and model output for auditability.",
        ]
        ids = [f"doc-{idx}" for idx in range(1, len(docs) + 1)]
        self._collection.add(documents=docs, ids=ids)

    def query_context(self, text: str, limit: int = 3) -> List[str]:
        if not text.strip():
            return []
        result = self._collection.query(query_texts=[text], n_results=limit)
        return result.get("documents", [[]])[0]

    def count(self) -> int:
        return self._collection.count()
