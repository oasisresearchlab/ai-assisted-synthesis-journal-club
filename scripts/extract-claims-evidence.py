#!/usr/bin/env python3
"""
Extract claims and evidence from papers CSV using Claude API.

This script:
1. Loads papers from CSV
2. Extracts evidence from each paper with What/How/Who notes
3. Generates individual paper markdown files (prefixed with @)
4. Synthesizes claims across all papers
5. Links claims to supporting evidence
"""

import os
import sys
import pandas as pd
import re
from pathlib import Path
from anthropic import Anthropic
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
CSV_PATH = "data/papers-llm-entailment-claim-verification.csv"
EVIDENCE_DIR = "evidence"
CLAIMS_DIR = "claims"
RESEARCH_QUESTION = """How effective are AI systems (ranging from older task-specific models
to LLMs and LLM-powered models) at the task of estimating entailment between claims
(e.g., for applications like claim verification and fact checking)?"""

# Substantive fields to extract evidence from
SUBSTANTIVE_FIELDS = [
    "AI Systems Tested",
    "Entailment Task Definition",
    "Evaluation Setup",
    "Performance Results",
    "Key Findings",
    "Contextual Factors"
]

# Supporting fields for each substantive field
SUPPORTING_QUOTE_FIELDS = [
    "Supporting quotes for \"AI Systems Tested\"",
    "Supporting quotes for \"Entailment Task Definition\"",
    "Supporting quotes for \"Evaluation Setup\"",
    "Supporting quotes for \"Performance Results\"",
    "Supporting quotes for \"Key Findings\"",
    "Supporting quotes for \"Contextual Factors\""
]


def sanitize_filename(title, year):
    """Create sanitized filename from paper title and year."""
    # Extract first author's last name from title (simplified approach)
    # For better accuracy, we'll use the Authors field
    return f"paper-{year}"


def sanitize_author_year(authors, year):
    """Create filename from first author's last name and year."""
    if pd.isna(authors) or not authors:
        return f"unknown-{year}"

    # Extract first author's last name
    first_author = authors.split(',')[0].strip()
    # Get last name (assuming "First Last" or "Last, First" format)
    if ',' in first_author:
        last_name = first_author.split(',')[0].strip()
    else:
        parts = first_author.split()
        last_name = parts[-1] if parts else "unknown"

    # Sanitize
    last_name = re.sub(r'[^a-zA-Z0-9]', '', last_name).lower()

    return f"@{last_name}-{year}"


def extract_evidence_from_paper(client, paper_data):
    """
    Use Claude API to extract evidence items from a single paper.
    Returns a list of evidence items with What/How/Who notes.
    """
    # Build context from paper fields
    paper_context = f"""
Paper: {paper_data['Title']}
Authors: {paper_data['Authors']}
Year: {paper_data['Year']}

Research Question Context: {RESEARCH_QUESTION}

Paper Data:
"""

    for field in SUBSTANTIVE_FIELDS:
        if field in paper_data and not pd.isna(paper_data[field]):
            paper_context += f"\n## {field}\n{paper_data[field]}\n"

    # Add supporting quotes if available
    for quote_field in SUPPORTING_QUOTE_FIELDS:
        if quote_field in paper_data and not pd.isna(paper_data[quote_field]):
            paper_context += f"\n## {quote_field}\n{paper_data[quote_field]}\n"

    prompt = f"""Given the following paper data, extract 3-10 discrete empirical evidence items
that address the research question about AI system effectiveness at entailment/claim verification.

{paper_context}

For each evidence item, provide:
1. A clear statement of the empirical finding/result
2. Three subbullet notes organized as:
   - **What**: Observable measures/data collected (e.g., accuracy metrics, performance scores)
   - **How**: Procedures/analyses/experimental design (e.g., prompting approaches, evaluation methods)
   - **Who**: Participants/dataset/population (e.g., dataset details, model types tested)

Return your response as a JSON array where each item has:
{{
  "evidence": "The main evidence statement",
  "what": "What was measured/collected",
  "how": "How it was measured/analyzed",
  "who": "Who/what dataset was used"
}}

Focus on discrete empirical results that could support or oppose broader claims about AI effectiveness
at entailment tasks. Include specific metrics, comparisons, and statistical evidence when available.
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parse the response
        response_text = response.content[0].text

        # Try to extract JSON from the response
        # Look for JSON array in the response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            evidence_items = json.loads(json_match.group(0))
            return evidence_items
        else:
            print(f"Warning: Could not parse JSON from response for {paper_data['Title']}")
            return []

    except Exception as e:
        print(f"Error extracting evidence from {paper_data['Title']}: {e}")
        return []


def generate_paper_markdown(paper_data, evidence_items, filename):
    """Generate markdown file for a single paper with evidence items."""

    content = f"""# {paper_data['Title']}

**Authors:** {paper_data['Authors']}
**Year:** {paper_data['Year']}
**DOI:** {paper_data.get('DOI', 'N/A')}
**Citation Count:** {paper_data.get('Citation count', 'N/A')}

## Evidence Items

"""

    for idx, item in enumerate(evidence_items, 1):
        evidence_id = f"evd-{idx:03d}"
        content += f"""- {item['evidence']} #evd-candidate ^{evidence_id}
\t- **What**: {item['what']}
\t- **How**: {item['how']}
\t- **Who**: {item['who']}
"""

    # Write to file
    filepath = os.path.join(EVIDENCE_DIR, filename + ".md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created {filepath}")

    return filepath


def synthesize_claims(client, all_evidence_data):
    """
    Use Claude API to synthesize claims across all evidence.
    Returns a list of claims with links to supporting evidence.
    """

    # Build evidence summary for claim synthesis
    evidence_summary = "# All Extracted Evidence\n\n"

    for paper_file, paper_title, evidence_items in all_evidence_data:
        evidence_summary += f"\n## From: {paper_title} ({paper_file})\n\n"
        for idx, item in enumerate(evidence_items, 1):
            evidence_id = f"evd-{idx:03d}"
            evidence_summary += f"- [{evidence_id}] {item['evidence']}\n"
            evidence_summary += f"  - What: {item['what']}\n"
            evidence_summary += f"  - How: {item['how']}\n"
            evidence_summary += f"  - Who: {item['who']}\n"

    prompt = f"""Given the following evidence extracted from multiple papers about AI systems'
effectiveness at entailment/claim verification, synthesize 5-15 high-level candidate claims.

Research Question: {RESEARCH_QUESTION}

{evidence_summary}

For each claim, identify which evidence items support it. Return as a JSON array where each item has:
{{
  "claim": "The synthesized claim statement",
  "supporting_evidence": [
    {{"paper_file": "@filename.md", "evidence_id": "evd-001"}},
    {{"paper_file": "@filename.md", "evidence_id": "evd-002"}}
  ]
}}

Generate claims that:
- Identify patterns across multiple papers
- Compare model types (e.g., closed vs open-source, LLMs vs task-specific)
- Address methodological patterns (e.g., prompting strategies, evaluation approaches)
- Note performance factors and moderators
- Highlight contradictions or nuances when present

Each claim should be supported by at least one evidence item.
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        response_text = response.content[0].text

        # Extract JSON
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            claims = json.loads(json_match.group(0))
            return claims
        else:
            print("Warning: Could not parse claims JSON from response")
            return []

    except Exception as e:
        print(f"Error synthesizing claims: {e}")
        return []


def generate_claims_markdown(claims):
    """Generate the central claims markdown file."""

    content = f"""# Candidate Claims

Research Question: {RESEARCH_QUESTION}

## Claims

"""

    for claim_data in claims:
        claim = claim_data['claim']

        # Build evidence links
        evidence_links = []
        for evd in claim_data['supporting_evidence']:
            paper_file = evd['paper_file']
            evidence_id = evd['evidence_id']
            evidence_links.append(f"[[evidence/{paper_file}#{evidence_id}]]")

        links_str = " ".join(evidence_links)
        content += f"- {claim} #clm-candidate {links_str}\n"

    # Write to file
    filepath = os.path.join(CLAIMS_DIR, "central-claims.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nCreated {filepath}")


def main():
    """Main extraction workflow."""

    print("Starting claims and evidence extraction...")
    print(f"Research Question: {RESEARCH_QUESTION}\n")

    # Initialize Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    # Load CSV
    print(f"Loading CSV from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} papers\n")

    # Process each paper
    all_evidence_data = []

    for idx, row in df.iterrows():
        print(f"\n[{idx + 1}/{len(df)}] Processing: {row['Title'][:60]}...")

        # Extract evidence
        evidence_items = extract_evidence_from_paper(client, row)

        if not evidence_items:
            print(f"  No evidence extracted, skipping...")
            continue

        print(f"  Extracted {len(evidence_items)} evidence items")

        # Generate filename
        filename = sanitize_author_year(row['Authors'], row['Year'])

        # Generate paper markdown
        generate_paper_markdown(row, evidence_items, filename)

        # Store for claim synthesis
        all_evidence_data.append((filename + ".md", row['Title'], evidence_items))

    print(f"\n\nGenerated {len(all_evidence_data)} paper evidence files")

    # Synthesize claims
    print("\n" + "="*60)
    print("Synthesizing claims across all evidence...")
    print("="*60 + "\n")

    claims = synthesize_claims(client, all_evidence_data)
    print(f"Synthesized {len(claims)} candidate claims")

    # Generate claims markdown
    generate_claims_markdown(claims)

    print("\n" + "="*60)
    print("Extraction complete!")
    print("="*60)
    print(f"\nOutput:")
    print(f"  - Evidence files: {EVIDENCE_DIR}/ ({len(all_evidence_data)} files)")
    print(f"  - Claims file: {CLAIMS_DIR}/central-claims.md ({len(claims)} claims)")


if __name__ == "__main__":
    main()
