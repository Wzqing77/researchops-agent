import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


class LocalRetriever:
    """
    ResearchOps 本地 HPC 文档检索器。

    流程：
        Markdown 文档
        → Chunk
        → Embedding
        → Cosine Similarity
        → Top-K
    """

    def __init__(
        self,
        knowledge_dir: Path,
        model_name: str = (
            "sentence-transformers/"
            "paraphrase-multilingual-MiniLM-L12-v2"
        ),
        chunk_size: int = 800,
    ):
        self.knowledge_dir = knowledge_dir
        self.chunk_size = chunk_size

        # 1. 加载 Embedding 模型
        self.model = SentenceTransformer(
            model_name
        )

        # 2. 读取知识库并切块
        self.chunks = self._load_documents()

        if not self.chunks:
            raise ValueError(
                "No knowledge documents found."
            )

        # 3. 为所有知识 Chunk 生成向量
        texts = [
            chunk["text"]
            for chunk in self.chunks
        ]

        self.embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

    def _load_documents(self) -> list[dict]:
        """
        读取 rag/knowledge/*.md。
        """

        chunks = []

        for path in sorted(
            self.knowledge_dir.glob("*.md")
        ):
            text = path.read_text(
                encoding="utf-8"
            )

            document_chunks = (
                self._chunk_text(text)
            )

            for index, chunk_text in enumerate(
                document_chunks
            ):
                chunks.append(
                    {
                        "source": path.name,
                        "chunk_id": index,
                        "text": chunk_text,
                    }
                )

        return chunks

    def _chunk_text(
        self,
        text: str,
    ) -> list[str]:
        """
        按段落切分，并尽量控制每个 Chunk
        不超过 chunk_size。
        """

        paragraphs = [
            part.strip()
            for part in re.split(
                r"\n\s*\n",
                text,
            )
            if part.strip()
        ]

        chunks = []
        current = ""

        for paragraph in paragraphs:
            if current:
                candidate = (
                    current
                    + "\n\n"
                    + paragraph
                )
            else:
                candidate = paragraph

            if len(candidate) <= self.chunk_size:
                current = candidate

            else:
                if current:
                    chunks.append(current)

                current = paragraph

        if current:
            chunks.append(current)

        return chunks

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        """
        根据 Query 找到最相关的 Top-K
        HPC 知识 Chunk。
        """

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        # 两边都已经 normalize，
        # 因此向量点积等价于 cosine similarity。
        scores = (
            self.embeddings
            @ query_embedding
        )

        top_indices = np.argsort(
            scores
        )[::-1][:top_k]

        results = []

        for index in top_indices:
            chunk = self.chunks[
                int(index)
            ]

            results.append(
                {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "score": float(
                        scores[index]
                    ),
                    "text": chunk["text"],
                }
            )

        return results