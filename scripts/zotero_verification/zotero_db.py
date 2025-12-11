"""Zotero SQLite database interface for mapping citekeys to PDF files."""

import sqlite3
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

from .config import ZOTERO_DB_PATH, ZOTERO_STORAGE_PATH


@dataclass
class PaperMetadata:
    """Metadata for a paper from Zotero."""
    item_id: int
    title: str
    authors: str
    year: str
    citekey: str


@dataclass
class PDFAttachment:
    """PDF attachment information."""
    path: Path
    metadata: PaperMetadata


class ZoteroDatabase:
    """Interface to Zotero SQLite database."""

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize connection to Zotero SQLite database.

        Args:
            db_path: Path to zotero.sqlite file. Defaults to config value.
        """
        self.db_path = db_path or ZOTERO_DB_PATH
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Zotero database not found at {self.db_path}\n"
                f"Please check your Zotero installation or set ZOTERO_DB_PATH "
                f"in your .env file."
            )

        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # Enable column access by name

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def find_pdf_by_citekey(self, citekey: str) -> Optional[PDFAttachment]:
        """
        Find PDF file path for a given citekey.

        Args:
            citekey: Citation key (e.g., 'yue-2024' or '@yue-2024')

        Returns:
            PDFAttachment with path and metadata, or None if not found

        Raises:
            ValueError: If multiple PDFs found for citekey
            FileNotFoundError: If PDF attachment path doesn't exist on disk
        """
        # Strip @ prefix if present
        clean_citekey = citekey.lstrip('@')

        # Get paper metadata
        metadata = self._get_paper_metadata(clean_citekey)
        if not metadata:
            # Try fuzzy matching
            suggestions = self._fuzzy_match_citekey(clean_citekey)
            if suggestions:
                raise ValueError(
                    f"Citekey '{clean_citekey}' not found in Zotero library.\n"
                    f"Did you mean: {', '.join(suggestions)}?"
                )
            else:
                raise ValueError(
                    f"Citekey '{clean_citekey}' not found in Zotero library."
                )

        # Find PDF attachments for this item
        pdf_paths = self._get_pdf_attachments(metadata.item_id)

        if not pdf_paths:
            raise FileNotFoundError(
                f"No PDF attachment found for citekey '{clean_citekey}'"
            )

        if len(pdf_paths) > 1:
            print(
                f"Warning: Multiple PDFs found for '{clean_citekey}'. "
                f"Using the first one: {pdf_paths[0]}"
            )

        pdf_path = pdf_paths[0]

        # Verify file exists on disk
        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found at {pdf_path}\n"
                f"The Zotero attachment may be broken or moved."
            )

        return PDFAttachment(path=pdf_path, metadata=metadata)

    def _get_paper_metadata(self, citekey: str) -> Optional[PaperMetadata]:
        """
        Retrieve paper metadata by citekey.

        Args:
            citekey: Citation key without @ prefix

        Returns:
            PaperMetadata or None if not found
        """
        # First try BetterBibTeX format (Extra field with "Citation Key: XXX")
        query_extra = """
        SELECT items.itemID, itemDataValues.value as fieldValue, fields.fieldName
        FROM items
        JOIN itemData ON items.itemID = itemData.itemID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        JOIN fields ON itemData.fieldID = fields.fieldID
        WHERE items.itemID IN (
            SELECT items.itemID FROM items
            JOIN itemData ON items.itemID = itemData.itemID
            JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
            JOIN fields ON itemData.fieldID = fields.fieldID
            WHERE fields.fieldName = 'extra'
            AND (itemDataValues.value LIKE 'Citation Key: ' || ? || '%'
                 OR itemDataValues.value LIKE '%
Citation Key: ' || ? || '%')
        )
        AND fields.fieldName IN ('extra', 'title', 'date')
        """

        cursor = self.conn.execute(query_extra, (citekey, citekey))
        rows = cursor.fetchall()

        # If not found, try standard citationKey field
        if not rows:
            query_standard = """
            SELECT items.itemID, itemDataValues.value as fieldValue, fields.fieldName
            FROM items
            JOIN itemData ON items.itemID = itemData.itemID
            JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
            JOIN fields ON itemData.fieldID = fields.fieldID
            WHERE items.itemID IN (
                SELECT items.itemID FROM items
                JOIN itemData ON items.itemID = itemData.itemID
                JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
                JOIN fields ON itemData.fieldID = fields.fieldID
                WHERE fields.fieldName = 'citationKey'
                AND itemDataValues.value = ?
            )
            AND fields.fieldName IN ('citationKey', 'title', 'date')
            """

            cursor = self.conn.execute(query_standard, (citekey,))
            rows = cursor.fetchall()

        if not rows:
            return None

        # Parse results into metadata
        item_id = rows[0]['itemID']
        title = None
        year = None
        citekey_confirmed = citekey

        for row in rows:
            field_name = row['fieldName']
            field_value = row['fieldValue']

            if field_name == 'title':
                title = field_value
            elif field_name == 'date':
                # Extract year from date (handle various formats)
                year = self._extract_year(field_value)
            elif field_name == 'extra':
                # Parse BetterBibTeX citation key from Extra field
                # Format: "Citation Key: XXX" (may be on its own line)
                import re
                match = re.search(r'Citation Key:\s*(\S+)', field_value)
                if match:
                    citekey_confirmed = match.group(1)
            elif field_name == 'citationKey':
                citekey_confirmed = field_value

        # Get authors separately (stored in creators table)
        authors = self._get_authors(item_id)

        return PaperMetadata(
            item_id=item_id,
            title=title or "Unknown",
            authors=authors or "Unknown",
            year=year or "Unknown",
            citekey=citekey_confirmed
        )

    def _get_authors(self, item_id: int) -> str:
        """Get comma-separated list of authors for an item."""
        query = """
        SELECT firstName, lastName
        FROM creators
        JOIN itemCreators ON creators.creatorID = itemCreators.creatorID
        WHERE itemCreators.itemID = ?
        ORDER BY itemCreators.orderIndex
        """

        cursor = self.conn.execute(query, (item_id,))
        rows = cursor.fetchall()

        authors = []
        for row in rows:
            first = row['firstName'] or ""
            last = row['lastName'] or ""
            name = f"{first} {last}".strip()
            if name:
                authors.append(name)

        return ", ".join(authors) if authors else "Unknown"

    def _extract_year(self, date_str: str) -> str:
        """Extract year from various date formats."""
        import re
        # Try to find a 4-digit year
        match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if match:
            return match.group(0)
        return "Unknown"

    def _get_pdf_attachments(self, item_id: int) -> List[Path]:
        """
        Get all PDF attachment paths for an item.

        Args:
            item_id: Zotero item ID

        Returns:
            List of paths to PDF files
        """
        query = """
        SELECT items.key, itemAttachments.path
        FROM itemAttachments
        JOIN items ON itemAttachments.itemID = items.itemID
        WHERE itemAttachments.parentItemID = ?
        AND itemAttachments.contentType = 'application/pdf'
        """

        cursor = self.conn.execute(query, (item_id,))
        rows = cursor.fetchall()

        pdf_paths = []
        for row in rows:
            attachment_key = row['key']
            attachment_path = row['path']

            if attachment_path:
                # Handle different path formats
                if attachment_path.startswith('storage:'):
                    # Internal Zotero storage
                    # Format: storage:filename.pdf
                    filename = attachment_path.replace('storage:', '')
                    full_path = ZOTERO_STORAGE_PATH / attachment_key / filename
                elif attachment_path.startswith('attachments:'):
                    # Linked attachment
                    filename = attachment_path.replace('attachments:', '')
                    full_path = ZOTERO_STORAGE_PATH.parent / 'attachments' / filename
                else:
                    # Absolute path
                    full_path = Path(attachment_path)

                pdf_paths.append(full_path)

        return pdf_paths

    def _fuzzy_match_citekey(self, citekey: str, limit: int = 3) -> List[str]:
        """
        Find similar citekeys using fuzzy matching.

        Args:
            citekey: The citekey to match
            limit: Maximum number of suggestions

        Returns:
            List of similar citekeys
        """
        try:
            import Levenshtein
        except ImportError:
            # If Levenshtein not available, skip fuzzy matching
            return []

        # Get all citekeys from database (both standard and BetterBibTeX)
        import re

        # Get BetterBibTeX citekeys from Extra field
        query_extra = """
        SELECT DISTINCT itemDataValues.value
        FROM itemData
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        JOIN fields ON itemData.fieldID = fields.fieldID
        WHERE fields.fieldName = 'extra'
        AND itemDataValues.value LIKE '%Citation Key:%'
        """
        cursor = self.conn.execute(query_extra)
        extra_rows = cursor.fetchall()

        all_citekeys = []
        for row in extra_rows:
            match = re.search(r'Citation Key:\s*(\S+)', row[0])
            if match:
                all_citekeys.append(match.group(1))

        # Get standard citekeys
        query_standard = """
        SELECT DISTINCT itemDataValues.value
        FROM itemData
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        JOIN fields ON itemData.fieldID = fields.fieldID
        WHERE fields.fieldName = 'citationKey'
        """

        cursor = self.conn.execute(query_standard)
        all_citekeys.extend([row[0] for row in cursor.fetchall()])

        # Calculate distances and sort
        distances = [
            (ck, Levenshtein.distance(citekey.lower(), ck.lower()))
            for ck in all_citekeys
        ]
        distances.sort(key=lambda x: x[1])

        # Return top matches (exclude exact matches and very different ones)
        return [ck for ck, dist in distances[:limit] if dist > 0 and dist <= 5]

    def list_all_citekeys(self) -> List[str]:
        """Get all citation keys in the Zotero library."""
        import re

        all_citekeys = []

        # Get BetterBibTeX citekeys from Extra field
        query_extra = """
        SELECT DISTINCT itemDataValues.value
        FROM itemData
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        JOIN fields ON itemData.fieldID = fields.fieldID
        WHERE fields.fieldName = 'extra'
        AND itemDataValues.value LIKE '%Citation Key:%'
        """
        cursor = self.conn.execute(query_extra)
        for row in cursor.fetchall():
            match = re.search(r'Citation Key:\s*(\S+)', row[0])
            if match:
                all_citekeys.append(match.group(1))

        # Get standard citekeys
        query_standard = """
        SELECT DISTINCT itemDataValues.value
        FROM itemData
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        JOIN fields ON itemData.fieldID = fields.fieldID
        WHERE fields.fieldName = 'citationKey'
        ORDER BY itemDataValues.value
        """

        cursor = self.conn.execute(query_standard)
        all_citekeys.extend([row[0] for row in cursor.fetchall()])

        return sorted(set(all_citekeys))
