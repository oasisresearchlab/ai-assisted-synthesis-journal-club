"""PDF text and image extraction using PyMuPDF."""

import re
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass

import fitz  # PyMuPDF

from .config import MAX_CHUNK_WORDS, CHUNK_OVERLAP_WORDS, IMAGE_DPI


@dataclass
class TextChunk:
    """A semantic chunk of text from a PDF."""
    content: str
    page_num: int
    chunk_id: str
    bbox: Optional[Tuple[float, float, float, float]] = None  # (x0, y0, x1, y1)


@dataclass
class Figure:
    """A figure or table extracted from a PDF."""
    type: str  # 'figure' or 'table'
    caption: str
    page_num: int
    image_path: Optional[Path] = None
    bbox: Optional[Tuple[float, float, float, float]] = None


class PDFExtractor:
    """Extract text chunks and figures from PDF files."""

    def __init__(self):
        """Initialize PDF extractor."""
        pass

    def extract_text_chunks(self, pdf_path: Path) -> List[TextChunk]:
        """
        Extract text in semantic chunks from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of TextChunk objects

        Raises:
            Exception: If PDF cannot be opened or is encrypted
        """
        try:
            doc = fitz.open(str(pdf_path))
        except Exception as e:
            raise Exception(f"Failed to open PDF: {e}")

        if doc.is_encrypted:
            print(f"Warning: PDF is encrypted. Attempting to extract with limited access...")

        chunks = []
        chunk_counter = 0

        for page_num in range(len(doc)):
            page = doc[page_num]

            # Extract text with layout preservation
            text = page.get_text("text")

            if not text.strip():
                continue  # Skip empty pages

            # Split into paragraphs (double newline or significant whitespace)
            paragraphs = self._split_into_paragraphs(text)

            # Create chunks from paragraphs with word limit and overlap
            page_chunks = self._create_chunks(
                paragraphs,
                page_num + 1,  # 1-indexed page numbers
                chunk_counter
            )

            chunks.extend(page_chunks)
            chunk_counter += len(page_chunks)

        doc.close()

        if not chunks:
            raise Exception("No text could be extracted from PDF. It may be scanned (no text layer).")

        return chunks

    def _split_into_paragraphs(self, text: str) -> List[str]:
        """
        Split text into paragraphs.

        Args:
            text: Raw text from PDF page

        Returns:
            List of paragraph strings
        """
        # Remove headers/footers (repeated single lines at top/bottom)
        # This is a simple heuristic - can be improved

        # Split by double newlines or multiple spaces followed by newline
        paragraphs = re.split(r'\n\s*\n', text)

        # Clean up each paragraph
        cleaned = []
        for para in paragraphs:
            # Remove extra whitespace
            para = re.sub(r'\s+', ' ', para).strip()
            # Skip very short paragraphs (likely headers/footers)
            if len(para.split()) > 5:  # At least 5 words
                cleaned.append(para)

        return cleaned

    def _create_chunks(
        self,
        paragraphs: List[str],
        page_num: int,
        start_counter: int
    ) -> List[TextChunk]:
        """
        Create chunks from paragraphs with word limits and overlap.

        Args:
            paragraphs: List of paragraph strings
            page_num: Page number (1-indexed)
            start_counter: Starting chunk counter

        Returns:
            List of TextChunk objects
        """
        chunks = []
        current_words = []
        current_text = []

        for para in paragraphs:
            words = para.split()

            # If adding this paragraph exceeds limit, create a chunk
            if len(current_words) + len(words) > MAX_CHUNK_WORDS and current_words:
                # Create chunk
                chunk_text = ' '.join(current_text)
                chunk_id = f"p{page_num}-chunk-{len(chunks)}"
                chunks.append(TextChunk(
                    content=chunk_text,
                    page_num=page_num,
                    chunk_id=chunk_id
                ))

                # Keep overlap words for context
                overlap_words = current_words[-CHUNK_OVERLAP_WORDS:] if len(current_words) > CHUNK_OVERLAP_WORDS else current_words
                current_words = overlap_words + words
                current_text = [' '.join(overlap_words), para]
            else:
                current_words.extend(words)
                current_text.append(para)

        # Add remaining text as final chunk
        if current_text:
            chunk_text = ' '.join(current_text)
            chunk_id = f"p{page_num}-chunk-{len(chunks)}"
            chunks.append(TextChunk(
                content=chunk_text,
                page_num=page_num,
                chunk_id=chunk_id
            ))

        return chunks

    def extract_figures_and_tables(
        self,
        pdf_path: Path,
        output_dir: Path
    ) -> List[Figure]:
        """
        Extract figures and tables with captions from PDF.

        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save extracted images

        Returns:
            List of Figure objects

        Raises:
            Exception: If PDF cannot be opened
        """
        try:
            doc = fitz.open(str(pdf_path))
        except Exception as e:
            raise Exception(f"Failed to open PDF: {e}")

        output_dir.mkdir(parents=True, exist_ok=True)
        figures = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")

            # Find figure and table captions
            caption_patterns = [
                (r'(Figure|Fig\.?)\s+(\d+)[:\.]?\s*(.{0,200})', 'figure'),
                (r'(Table|TABLE)\s+(\d+)[:\.]?\s*(.{0,200})', 'table'),
            ]

            for pattern, fig_type in caption_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)

                for match in matches:
                    full_match = match.group(0)
                    number = match.group(2)
                    caption_text = match.group(3).strip() if match.group(3) else ""

                    # Create figure object
                    figure = Figure(
                        type=fig_type,
                        caption=full_match,
                        page_num=page_num + 1
                    )

                    # Try to extract image for this figure/table
                    # For Phase 1 (text-only), we'll skip actual image extraction
                    # This will be implemented in Phase 2
                    # image_path = self._extract_figure_image(
                    #     page, number, fig_type, output_dir
                    # )
                    # figure.image_path = image_path

                    figures.append(figure)

        doc.close()
        return figures

    def _extract_figure_image(
        self,
        page: fitz.Page,
        number: str,
        fig_type: str,
        output_dir: Path
    ) -> Optional[Path]:
        """
        Extract image for a specific figure or table.

        Note: This is a placeholder for Phase 2 implementation.
        Full implementation will locate figure region and render as PNG.
        """
        # Phase 2: Implement actual image extraction
        # 1. Locate the figure/table region on the page
        # 2. Extract bounding box
        # 3. Render region as high-res PNG
        # 4. Save to output_dir with appropriate naming
        return None

    def get_page_count(self, pdf_path: Path) -> int:
        """Get the number of pages in a PDF."""
        try:
            doc = fitz.open(str(pdf_path))
            count = len(doc)
            doc.close()
            return count
        except Exception:
            return 0
