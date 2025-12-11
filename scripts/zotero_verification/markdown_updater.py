"""Markdown file manipulation for adding verification sections."""

import re
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass

from .semantic_search import ScoredChunk
from .pdf_extractor import Figure


@dataclass
class VerificationSnippets:
    """Container for verification snippets to add to markdown."""
    node_id: str
    text_quotes: List[ScoredChunk]
    figures: List[Figure]
    metadata: Dict


class MarkdownUpdater:
    """Update evidence markdown files with verification sections."""

    def __init__(self, evidence_dir: Path, attachments_dir: Path):
        """
        Initialize markdown updater.

        Args:
            evidence_dir: Directory containing evidence markdown files
            attachments_dir: Directory for storing verification images
        """
        self.evidence_dir = evidence_dir
        self.attachments_dir = attachments_dir

    def add_verification_section(
        self,
        citekey: str,
        snippets: VerificationSnippets,
        dry_run: bool = False
    ) -> bool:
        """
        Add or update verification section for a node in markdown file.

        Args:
            citekey: Paper citekey (e.g., '@yue-2024')
            snippets: Verification snippets to add
            dry_run: If True, print changes without writing

        Returns:
            True if successful, False otherwise
        """
        # Construct markdown file path
        markdown_path = self.evidence_dir / f"{citekey}.md"

        if not markdown_path.exists():
            print(f"Error: Markdown file not found: {markdown_path}")
            return False

        # Read existing content
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the node by block anchor
        node_pattern = rf"\^{re.escape(snippets.node_id)}"
        if not re.search(node_pattern, content):
            print(f"Error: Node anchor ^{snippets.node_id} not found in {citekey}.md")
            return False

        # Check if verification section already exists
        verification_header = f"### Verification Snippets ({snippets.node_id})"
        has_existing = verification_header in content

        # Generate verification section
        verification_section = self._format_verification_section(
            snippets,
            citekey
        )

        # Update content
        if has_existing:
            # Replace existing verification section
            updated_content = self._replace_verification_section(
                content,
                snippets.node_id,
                verification_section
            )
        else:
            # Insert new verification section after node
            updated_content = self._insert_verification_section(
                content,
                snippets.node_id,
                verification_section
            )

        if dry_run:
            print(f"\n{'='*60}")
            print(f"Dry run for {citekey}.md - Node: {snippets.node_id}")
            print(f"{'='*60}")
            print(verification_section)
            print(f"{'='*60}\n")
            return True

        # Backup original file
        backup_path = markdown_path.with_suffix('.md.backup')
        shutil.copy(markdown_path, backup_path)

        try:
            # Write updated content
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            # Remove backup on success
            backup_path.unlink()
            return True

        except Exception as e:
            print(f"Error writing markdown file: {e}")
            # Restore from backup
            shutil.copy(backup_path, markdown_path)
            backup_path.unlink()
            return False

    def _format_verification_section(
        self,
        snippets: VerificationSnippets,
        citekey: str
    ) -> str:
        """Format verification section content."""
        sections = []

        # Header
        sections.append(f"### Verification Snippets ({snippets.node_id})\n")

        # Text quotes
        if snippets.text_quotes:
            sections.append("**Text Quotes:**\n")
            for scored_chunk in snippets.text_quotes:
                chunk = scored_chunk.chunk
                quote = self._format_quote(chunk.content)
                page_ref = f"*— Page {chunk.page_num}*"
                sections.append(f"> {quote}\n>\n> {page_ref}\n")

        # Figures (if any)
        if snippets.figures:
            sections.append("**Figures/Tables:**\n")
            for figure in snippets.figures:
                if figure.image_path:
                    # For Phase 1, we don't have actual images yet
                    # This will be implemented in Phase 2
                    rel_path = f"attachments/verification/{citekey}/{figure.image_path.name}"
                    sections.append(f"![[{rel_path}]]\n")
                sections.append(f"*{figure.caption} (Page {figure.page_num})*\n")

        # Metadata
        sections.append("\n**Search Metadata:**")
        sections.append(f"- Verified: {snippets.metadata.get('verified_date', 'Unknown')}")
        sections.append(f"- Chunks searched: {snippets.metadata.get('chunks_searched', 0)}")

        snippets_found = []
        if snippets.text_quotes:
            snippets_found.append(f"{len(snippets.text_quotes)} text")
        if snippets.figures:
            snippets_found.append(f"{len(snippets.figures)} figure/table")

        if snippets_found:
            sections.append(f"- Relevant snippets found: {', '.join(snippets_found)}")
        else:
            sections.append("- Relevant snippets found: None")

        sections.append("\n---\n")

        return '\n'.join(sections)

    def _format_quote(self, text: str, max_length: int = 400) -> str:
        """Format a quote, truncating if too long."""
        # Clean up whitespace
        text = ' '.join(text.split())

        if len(text) <= max_length:
            return text

        # Truncate at word boundary
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]

        return f"{truncated}..."

    def _insert_verification_section(
        self,
        content: str,
        node_id: str,
        verification_section: str
    ) -> str:
        """
        Insert verification section after a node.

        Strategy: Find the node's block anchor, then insert after the node's
        metadata (What/How/Who bullets if Evidence node) or after the main content line.
        """
        lines = content.split('\n')
        updated_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            updated_lines.append(line)

            # Check if this line contains the node anchor
            if f"^{node_id}" in line:
                # Look ahead for What/How/Who metadata
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('-'):
                    # This is metadata (sub-bullet)
                    metadata_line = lines[j]
                    updated_lines.append(metadata_line)

                    # Check if metadata has further sub-bullets (What/How/Who)
                    k = j + 1
                    while k < len(lines) and lines[k].strip().startswith('-'):
                        if lines[k].startswith('\t-') or lines[k].startswith('  -'):
                            updated_lines.append(lines[k])
                            k += 1
                        else:
                            break
                    j = k

                # Insert verification section here
                updated_lines.append("")  # Blank line
                updated_lines.append(verification_section)

                # Skip the lines we already processed
                i = j - 1

            i += 1

        return '\n'.join(updated_lines)

    def _replace_verification_section(
        self,
        content: str,
        node_id: str,
        new_section: str
    ) -> str:
        """Replace existing verification section for a node."""
        # Find and remove existing verification section
        header_pattern = f"### Verification Snippets \\({re.escape(node_id)}\\)"
        lines = content.split('\n')
        updated_lines = []
        i = 0
        skip_until_separator = False

        while i < len(lines):
            line = lines[i]

            # Check if this is the verification header to replace
            if re.match(header_pattern, line):
                # Skip until we hit the separator (---) or next major section
                skip_until_separator = True
                i += 1
                continue

            if skip_until_separator:
                # Stop skipping when we hit separator or next section
                if line.strip() == '---' or line.startswith('## ') or line.startswith('- ') and not line.startswith('  '):
                    skip_until_separator = False
                    # Insert new section before moving on
                    updated_lines.append("")
                    updated_lines.append(new_section)
                    # Skip the --- separator line
                    i += 1
                    continue
                else:
                    # Still inside old verification section, skip
                    i += 1
                    continue

            updated_lines.append(line)
            i += 1

        return '\n'.join(updated_lines)

    def get_all_node_ids(self, citekey: str) -> List[str]:
        """
        Extract all node IDs from a markdown file.

        Args:
            citekey: Paper citekey (e.g., '@yue-2024')

        Returns:
            List of node IDs (e.g., ['evidence-000', 'claim-001'])
        """
        markdown_path = self.evidence_dir / f"{citekey}.md"

        if not markdown_path.exists():
            return []

        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all block anchors
        anchor_pattern = r'\^([a-z]+-\d+)'
        matches = re.findall(anchor_pattern, content)

        return matches

    def get_node_content(self, citekey: str, node_id: str) -> Optional[Dict]:
        """
        Extract node content and metadata.

        Args:
            citekey: Paper citekey
            node_id: Node ID (e.g., 'evidence-000')

        Returns:
            Dict with 'content', 'type', 'metadata' or None if not found
        """
        markdown_path = self.evidence_dir / f"{citekey}.md"

        if not markdown_path.exists():
            return None

        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the line with this node anchor
        anchor_pattern = rf'^- (.+?) #\w+-candidate \^{re.escape(node_id)}'
        match = re.search(anchor_pattern, content, re.MULTILINE)

        if not match:
            return None

        node_content = match.group(1)

        # Determine node type from ID prefix
        node_type = node_id.split('-')[0].capitalize()

        # Extract metadata (What/How/Who for Evidence nodes)
        metadata = {}
        lines = content.split('\n')
        start_idx = content[:match.start()].count('\n')

        # Look for metadata in following lines
        for i in range(start_idx + 1, min(start_idx + 10, len(lines))):
            line = lines[i]
            if line.strip().startswith('- **What**:'):
                metadata['what'] = line.split(':', 1)[1].strip()
            elif line.strip().startswith('- **How**:'):
                metadata['how'] = line.split(':', 1)[1].strip()
            elif line.strip().startswith('- **Who**:'):
                metadata['who'] = line.split(':', 1)[1].strip()
            elif not line.strip().startswith('-'):
                # End of metadata
                break

        return {
            'content': node_content,
            'type': node_type,
            'metadata': metadata
        }
