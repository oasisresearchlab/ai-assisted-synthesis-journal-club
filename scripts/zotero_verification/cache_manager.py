"""Caching layer for PDF extractions and LLM scores."""

import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from .config import PDF_CACHE_DIR, LLM_CACHE_DIR, CACHE_EXPIRY_DAYS
from .pdf_extractor import TextChunk, Figure


class CacheManager:
    """Manage caching of PDF extractions and LLM scores."""

    def __init__(self, pdf_cache_dir: Optional[Path] = None, llm_cache_dir: Optional[Path] = None):
        """
        Initialize cache manager.

        Args:
            pdf_cache_dir: Directory for PDF extraction cache
            llm_cache_dir: Directory for LLM score cache
        """
        self.pdf_cache_dir = pdf_cache_dir or PDF_CACHE_DIR
        self.llm_cache_dir = llm_cache_dir or LLM_CACHE_DIR

        # Ensure cache directories exist
        self.pdf_cache_dir.mkdir(parents=True, exist_ok=True)
        self.llm_cache_dir.mkdir(parents=True, exist_ok=True)

    def get_pdf_extraction(
        self,
        citekey: str,
        pdf_path: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached PDF extraction if valid.

        Args:
            citekey: Paper citekey
            pdf_path: Path to PDF file

        Returns:
            Cached extraction data or None if not cached or invalid
        """
        cache_file = self.pdf_cache_dir / f"{citekey}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Validate cache
            cached_hash = cache_data.get('pdf_hash')
            current_hash = self._compute_file_hash(pdf_path)

            if cached_hash != current_hash:
                # PDF has changed, invalidate cache
                print(f"Cache invalidated for {citekey} (PDF modified)")
                cache_file.unlink()
                return None

            # Cache is valid
            return cache_data

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Corrupted cache file for {citekey}: {e}")
            cache_file.unlink()
            return None

    def save_pdf_extraction(
        self,
        citekey: str,
        pdf_path: Path,
        text_chunks: List[TextChunk],
        figures: List[Figure],
        metadata: Dict[str, Any]
    ):
        """
        Save PDF extraction to cache.

        Args:
            citekey: Paper citekey
            pdf_path: Path to PDF file
            text_chunks: Extracted text chunks
            figures: Extracted figures
            metadata: Additional metadata
        """
        cache_file = self.pdf_cache_dir / f"{citekey}.json"

        # Compute PDF hash for validation
        pdf_hash = self._compute_file_hash(pdf_path)

        # Serialize data
        cache_data = {
            'citekey': citekey,
            'pdf_path': str(pdf_path),
            'pdf_hash': pdf_hash,
            'extracted_at': datetime.now().isoformat(),
            'text_chunks': [
                {
                    'content': chunk.content,
                    'page_num': chunk.page_num,
                    'chunk_id': chunk.chunk_id,
                    'bbox': chunk.bbox
                }
                for chunk in text_chunks
            ],
            'figures': [
                {
                    'type': fig.type,
                    'caption': fig.caption,
                    'page_num': fig.page_num,
                    'image_path': str(fig.image_path) if fig.image_path else None,
                    'bbox': fig.bbox
                }
                for fig in figures
            ],
            'metadata': metadata
        }

        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save cache for {citekey}: {e}")

    def get_llm_score(
        self,
        citekey: str,
        node_id: str,
        chunk_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached LLM score for a node-chunk pair.

        Args:
            citekey: Paper citekey
            node_id: Node ID
            chunk_id: Chunk ID

        Returns:
            Cached score data or None if not cached or expired
        """
        cache_key = self._generate_llm_cache_key(citekey, node_id, chunk_id)
        cache_file = self.llm_cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Check expiry
            cached_date = datetime.fromisoformat(cache_data['cached_at'])
            expiry_date = cached_date + timedelta(days=CACHE_EXPIRY_DAYS)

            if datetime.now() > expiry_date:
                # Cache expired
                cache_file.unlink()
                return None

            return cache_data

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Warning: Corrupted LLM cache file {cache_key}: {e}")
            cache_file.unlink()
            return None

    def save_llm_score(
        self,
        citekey: str,
        node_id: str,
        chunk_id: str,
        score: float,
        reasoning: str
    ):
        """
        Save LLM score to cache.

        Args:
            citekey: Paper citekey
            node_id: Node ID
            chunk_id: Chunk ID
            score: Relevance score
            reasoning: Reasoning for score
        """
        cache_key = self._generate_llm_cache_key(citekey, node_id, chunk_id)
        cache_file = self.llm_cache_dir / f"{cache_key}.json"

        cache_data = {
            'citekey': citekey,
            'node_id': node_id,
            'chunk_id': chunk_id,
            'score': score,
            'reasoning': reasoning,
            'cached_at': datetime.now().isoformat()
        }

        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save LLM cache for {cache_key}: {e}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA-256 hash of a file."""
        sha256 = hashlib.sha256()

        try:
            with open(file_path, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"Warning: Failed to compute hash for {file_path}: {e}")
            return ""

    def _generate_llm_cache_key(
        self,
        citekey: str,
        node_id: str,
        chunk_id: str
    ) -> str:
        """Generate cache key for LLM score."""
        # Create a hash of the components
        key_str = f"{citekey}_{node_id}_{chunk_id}"
        key_hash = hashlib.md5(key_str.encode()).hexdigest()[:16]
        return f"{citekey}_{node_id}_{key_hash}"

    def clear_pdf_cache(self, citekey: Optional[str] = None):
        """
        Clear PDF extraction cache.

        Args:
            citekey: If provided, clear only this paper's cache. Otherwise clear all.
        """
        if citekey:
            cache_file = self.pdf_cache_dir / f"{citekey}.json"
            if cache_file.exists():
                cache_file.unlink()
                print(f"Cleared PDF cache for {citekey}")
        else:
            for cache_file in self.pdf_cache_dir.glob("*.json"):
                cache_file.unlink()
            print("Cleared all PDF cache")

    def clear_llm_cache(self, citekey: Optional[str] = None):
        """
        Clear LLM score cache.

        Args:
            citekey: If provided, clear only this paper's cache. Otherwise clear all.
        """
        if citekey:
            for cache_file in self.llm_cache_dir.glob(f"{citekey}_*.json"):
                cache_file.unlink()
            print(f"Cleared LLM cache for {citekey}")
        else:
            for cache_file in self.llm_cache_dir.glob("*.json"):
                cache_file.unlink()
            print("Cleared all LLM cache")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        pdf_cache_count = len(list(self.pdf_cache_dir.glob("*.json")))
        llm_cache_count = len(list(self.llm_cache_dir.glob("*.json")))

        # Calculate total cache size
        pdf_cache_size = sum(
            f.stat().st_size for f in self.pdf_cache_dir.glob("*.json")
        )
        llm_cache_size = sum(
            f.stat().st_size for f in self.llm_cache_dir.glob("*.json")
        )

        return {
            'pdf_cache_entries': pdf_cache_count,
            'llm_cache_entries': llm_cache_count,
            'pdf_cache_size_mb': pdf_cache_size / (1024 * 1024),
            'llm_cache_size_mb': llm_cache_size / (1024 * 1024),
            'total_size_mb': (pdf_cache_size + llm_cache_size) / (1024 * 1024)
        }
