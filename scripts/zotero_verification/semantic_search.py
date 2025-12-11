"""LLM-based semantic search for relevant PDF chunks."""

import json
import time
from typing import List, Dict, Optional
from dataclasses import dataclass

from anthropic import Anthropic

from .pdf_extractor import TextChunk
from .config import (
    ANTHROPIC_API_KEY,
    DEFAULT_MODEL,
    MAX_RETRIES,
    RETRY_DELAY,
    DEFAULT_TOP_K,
    KEYWORD_PREFILTER_RATIO
)


@dataclass
class ScoredChunk:
    """A text chunk with relevance score and reasoning."""
    chunk: TextChunk
    relevance_score: float  # 0-10
    reasoning: str


class SemanticSearch:
    """LLM-based semantic search for finding relevant PDF passages."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize semantic search with Claude API.

        Args:
            api_key: Anthropic API key. Defaults to config value.
        """
        self.client = Anthropic(api_key=api_key or ANTHROPIC_API_KEY)

    def find_relevant_chunks(
        self,
        node_content: str,
        node_type: str,
        pdf_chunks: List[TextChunk],
        top_k: int = DEFAULT_TOP_K,
        use_keyword_filter: bool = True
    ) -> List[ScoredChunk]:
        """
        Find PDF chunks most relevant to a discourse node.

        Args:
            node_content: The text content of the node
            node_type: Type of node (Evidence, Claim, etc.)
            pdf_chunks: List of text chunks from PDF
            top_k: Number of top relevant chunks to return
            use_keyword_filter: Whether to pre-filter with keywords

        Returns:
            List of ScoredChunk objects, sorted by relevance (highest first)
        """
        if not pdf_chunks:
            return []

        # Phase 1: Keyword pre-filtering (optional optimization)
        if use_keyword_filter and len(pdf_chunks) > 30:
            filtered_chunks = self._keyword_prefilter(node_content, pdf_chunks)
        else:
            filtered_chunks = pdf_chunks

        # Phase 2: LLM-based scoring in batches
        all_scored = []
        batch_size = 25  # Process chunks in batches

        for i in range(0, len(filtered_chunks), batch_size):
            batch = filtered_chunks[i:i + batch_size]
            batch_scored = self._score_batch(node_content, node_type, batch)
            all_scored.extend(batch_scored)

        # Sort by relevance score (highest first)
        all_scored.sort(key=lambda x: x.relevance_score, reverse=True)

        # Phase 3: Re-rank top candidates for final selection (optional refinement)
        if len(all_scored) > top_k * 2:
            top_candidates = all_scored[:top_k * 2]
            refined = self._rerank_candidates(node_content, node_type, top_candidates, top_k)
            return refined

        return all_scored[:top_k]

    def _keyword_prefilter(
        self,
        node_content: str,
        chunks: List[TextChunk]
    ) -> List[TextChunk]:
        """
        Pre-filter chunks by keyword overlap.

        Args:
            node_content: Node text to extract keywords from
            chunks: All PDF chunks

        Returns:
            Filtered list of chunks (top 50% by keyword overlap)
        """
        # Extract significant words (remove common words)
        import re
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'we', 'they', 'our', 'their'
        }

        # Get keywords from node
        words = re.findall(r'\b\w+\b', node_content.lower())
        keywords = set(w for w in words if len(w) > 3 and w not in stop_words)

        # Score chunks by keyword overlap
        scored_chunks = []
        for chunk in chunks:
            chunk_words = set(re.findall(r'\b\w+\b', chunk.content.lower()))
            overlap = len(keywords & chunk_words)
            scored_chunks.append((chunk, overlap))

        # Sort by overlap score
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        # Return top 50%
        keep_count = max(1, int(len(scored_chunks) * KEYWORD_PREFILTER_RATIO))
        return [chunk for chunk, score in scored_chunks[:keep_count]]

    def _score_batch(
        self,
        node_content: str,
        node_type: str,
        chunks: List[TextChunk]
    ) -> List[ScoredChunk]:
        """
        Score a batch of chunks using LLM.

        Args:
            node_content: Node text
            node_type: Node type (Evidence, Claim, etc.)
            chunks: Batch of chunks to score

        Returns:
            List of ScoredChunk objects
        """
        # Build prompt
        prompt = self._build_scoring_prompt(node_content, node_type, chunks)

        # Call Claude API with retries
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.messages.create(
                    model=DEFAULT_MODEL,
                    max_tokens=4000,
                    temperature=0,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                # Parse JSON response
                response_text = response.content[0].text
                scores = self._parse_scores(response_text)

                # Create ScoredChunk objects
                scored_chunks = []
                for i, chunk in enumerate(chunks):
                    if i < len(scores):
                        score_data = scores[i]
                        scored_chunks.append(ScoredChunk(
                            chunk=chunk,
                            relevance_score=score_data.get('score', 0.0),
                            reasoning=score_data.get('reasoning', '')
                        ))
                    else:
                        # Fallback if not enough scores returned
                        scored_chunks.append(ScoredChunk(
                            chunk=chunk,
                            relevance_score=0.0,
                            reasoning="Not scored"
                        ))

                return scored_chunks

            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    print(f"Warning: Failed to score batch after {MAX_RETRIES} attempts: {e}")
                    # Return zero scores as fallback
                    return [
                        ScoredChunk(chunk=chunk, relevance_score=0.0, reasoning="Scoring failed")
                        for chunk in chunks
                    ]

    def _build_scoring_prompt(
        self,
        node_content: str,
        node_type: str,
        chunks: List[TextChunk]
    ) -> str:
        """Build prompt for scoring chunks."""
        # Format chunks for prompt
        chunks_text = ""
        for i, chunk in enumerate(chunks):
            chunks_text += f"\n[Chunk {i}] (Page {chunk.page_num}):\n{chunk.content}\n"

        prompt = f"""You are helping verify extracted discourse nodes from research papers by finding relevant passages in the source PDF.

**Node to Verify:**
Type: {node_type}
Content: "{node_content}"

**PDF Passages to Evaluate:**
{chunks_text}

**Task:**
Rate each passage from 0-10 for relevance to the node above. Consider:
- Does it provide factual support or evidence for the node?
- Does it contain methodological details related to the node?
- Does it contradict or oppose the node?
- Does it provide contextual information that helps understand the node?

A score of 0 means completely irrelevant, 10 means highly relevant and directly supports/relates to the node.

**Response Format:**
Return a JSON array with one object per chunk:
[
  {{"chunk_id": 0, "score": 8.5, "reasoning": "Brief explanation"}},
  {{"chunk_id": 1, "score": 3.0, "reasoning": "Brief explanation"}},
  ...
]

Respond only with the JSON array, no other text."""

        return prompt

    def _parse_scores(self, response_text: str) -> List[Dict]:
        """Parse JSON scores from LLM response."""
        try:
            # Try to extract JSON from response (handle markdown code blocks)
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
                scores = json.loads(json_text)
                return scores
            else:
                return []
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse LLM response as JSON: {e}")
            return []

    def _rerank_candidates(
        self,
        node_content: str,
        node_type: str,
        candidates: List[ScoredChunk],
        top_k: int
    ) -> List[ScoredChunk]:
        """
        Re-rank top candidates for final selection.

        This is an optional refinement step that compares candidates directly
        to select the most diverse and relevant set.
        """
        # For Phase 1, just return top candidates
        # Phase 2 could implement more sophisticated re-ranking
        return candidates[:top_k]
