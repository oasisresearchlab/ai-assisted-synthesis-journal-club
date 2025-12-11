#!/usr/bin/env python3
"""
CLI tool to verify extracted discourse nodes with PDF snippets from Zotero.

Usage:
    python scripts/verify_with_zotero.py @yue-2024
    python scripts/verify_with_zotero.py @yue-2024 --node evidence-000
    python scripts/verify_with_zotero.py @yue-2024 --type Evidence
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from zotero_verification.config import (
    EVIDENCE_DIR,
    ATTACHMENTS_DIR,
    ZOTERO_DB_PATH,
    DEFAULT_TOP_K
)
from zotero_verification.zotero_db import ZoteroDatabase
from zotero_verification.pdf_extractor import PDFExtractor, TextChunk, Figure
from zotero_verification.semantic_search import SemanticSearch
from zotero_verification.markdown_updater import MarkdownUpdater, VerificationSnippets
from zotero_verification.cache_manager import CacheManager


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Verify evidence nodes with PDF snippets from Zotero",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify all nodes in a paper
  python scripts/verify_with_zotero.py @yue-2024

  # Verify specific node
  python scripts/verify_with_zotero.py @yue-2024 --node evidence-000

  # Verify all Evidence nodes
  python scripts/verify_with_zotero.py @yue-2024 --type Evidence

  # Batch verify multiple papers
  python scripts/verify_with_zotero.py @yue-2024 @pham-2025

  # Configuration options
  python scripts/verify_with_zotero.py @yue-2024 --top-k 10 --dry-run
        """
    )

    # Required arguments
    parser.add_argument(
        'citekeys',
        nargs='+',
        help='Paper citekeys (e.g., @yue-2024)'
    )

    # Filtering options
    parser.add_argument(
        '--node',
        help='Specific node ID to verify (e.g., evidence-000)'
    )
    parser.add_argument(
        '--type',
        choices=['Evidence', 'Claim', 'Question', 'Pattern', 'Artifact'],
        help='Verify only nodes of this type'
    )

    # Configuration
    parser.add_argument(
        '--zotero-db',
        type=Path,
        default=ZOTERO_DB_PATH,
        help=f'Path to Zotero SQLite database (default: {ZOTERO_DB_PATH})'
    )
    parser.add_argument(
        '--top-k',
        type=int,
        default=DEFAULT_TOP_K,
        help=f'Number of text snippets to extract per node (default: {DEFAULT_TOP_K})'
    )
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Force re-extraction from PDFs (ignore cache)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show verification snippets without updating files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed extraction progress'
    )

    args = parser.parse_args()

    # Initialize components
    print("Initializing verification system...")
    zotero_db = ZoteroDatabase(args.zotero_db)
    pdf_extractor = PDFExtractor()
    semantic_search = SemanticSearch()
    markdown_updater = MarkdownUpdater(EVIDENCE_DIR, ATTACHMENTS_DIR)
    cache_manager = CacheManager()

    # Process each citekey
    total_verified = 0
    total_failed = 0

    for citekey in args.citekeys:
        print(f"\n{'='*60}")
        print(f"Verifying {citekey}...")
        print(f"{'='*60}")

        try:
            # Step 1: Locate PDF in Zotero
            print(f"  [1/4] Locating PDF in Zotero...", end=' ')
            pdf_attachment = zotero_db.find_pdf_by_citekey(citekey)
            print(f"✓")
            if args.verbose:
                print(f"        PDF: {pdf_attachment.path}")
                print(f"        Title: {pdf_attachment.metadata.title}")

            # Step 2: Extract text and images from PDF
            print(f"  [2/4] Extracting text from PDF...", end=' ')

            # Check cache first
            cached_extraction = None
            if not args.no_cache:
                cached_extraction = cache_manager.get_pdf_extraction(
                    citekey,
                    pdf_attachment.path
                )

            if cached_extraction:
                print("✓ (cached)")
                # Reconstruct objects from cache
                text_chunks = [
                    TextChunk(**chunk_data)
                    for chunk_data in cached_extraction['text_chunks']
                ]
                figures = [
                    Figure(**fig_data)
                    for fig_data in cached_extraction['figures']
                ]
            else:
                text_chunks = pdf_extractor.extract_text_chunks(pdf_attachment.path)
                figures = pdf_extractor.extract_figures_and_tables(
                    pdf_attachment.path,
                    ATTACHMENTS_DIR / citekey
                )
                print(f"✓ ({len(text_chunks)} chunks, {len(figures)} figures/tables)")

                # Save to cache
                cache_manager.save_pdf_extraction(
                    citekey,
                    pdf_attachment.path,
                    text_chunks,
                    figures,
                    {'page_count': pdf_extractor.get_page_count(pdf_attachment.path)}
                )

            # Step 3: Get nodes to verify
            print(f"  [3/4] Finding nodes to verify...", end=' ')

            if args.node:
                # Verify specific node
                node_ids = [args.node]
            else:
                # Get all nodes (optionally filtered by type)
                all_node_ids = markdown_updater.get_all_node_ids(citekey)

                if args.type:
                    # Filter by type
                    type_prefix = args.type.lower()
                    node_ids = [nid for nid in all_node_ids if nid.startswith(type_prefix)]
                else:
                    node_ids = all_node_ids

            print(f"✓ ({len(node_ids)} nodes)")

            if not node_ids:
                print(f"  No nodes found to verify.")
                continue

            # Step 4: Verify each node
            print(f"  [4/4] Finding relevant snippets...")

            verified_count = 0
            for node_id in node_ids:
                if args.verbose:
                    print(f"\n    Processing {node_id}...")

                # Get node content
                node_data = markdown_updater.get_node_content(citekey, node_id)
                if not node_data:
                    print(f"    Warning: Could not extract content for {node_id}")
                    continue

                # Find relevant chunks
                scored_chunks = semantic_search.find_relevant_chunks(
                    node_data['content'],
                    node_data['type'],
                    text_chunks,
                    top_k=args.top_k
                )

                if args.verbose:
                    print(f"    Found {len(scored_chunks)} relevant snippets")
                    for i, scored in enumerate(scored_chunks[:3], 1):
                        print(f"      {i}. Page {scored.chunk.page_num} (score: {scored.relevance_score:.1f})")

                # Create verification snippets
                snippets = VerificationSnippets(
                    node_id=node_id,
                    text_quotes=scored_chunks,
                    figures=[],  # Phase 2: Match figures to nodes
                    metadata={
                        'verified_date': datetime.now().strftime('%Y-%m-%d'),
                        'chunks_searched': len(text_chunks),
                        'figures_available': len(figures)
                    }
                )

                # Add to markdown
                success = markdown_updater.add_verification_section(
                    citekey,
                    snippets,
                    dry_run=args.dry_run
                )

                if success:
                    verified_count += 1

            if not args.dry_run:
                print(f"\n  ✓ Updated: evidence/{citekey}.md")
                print(f"    - {verified_count} node(s) verified")

            total_verified += verified_count

        except FileNotFoundError as e:
            print(f"\n  ✗ Error: {e}")
            total_failed += 1
        except ValueError as e:
            print(f"\n  ✗ Error: {e}")
            total_failed += 1
        except Exception as e:
            print(f"\n  ✗ Unexpected error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            total_failed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Papers processed: {len(args.citekeys)}")
    print(f"  Nodes verified: {total_verified}")
    if total_failed > 0:
        print(f"  Failures: {total_failed}")
    print(f"{'='*60}\n")

    # Show cache stats
    if args.verbose:
        stats = cache_manager.get_cache_stats()
        print(f"Cache statistics:")
        print(f"  PDF cache entries: {stats['pdf_cache_entries']}")
        print(f"  LLM cache entries: {stats['llm_cache_entries']}")
        print(f"  Total cache size: {stats['total_size_mb']:.2f} MB\n")

    zotero_db.close()

    # Exit with error code if any failures
    if total_failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
