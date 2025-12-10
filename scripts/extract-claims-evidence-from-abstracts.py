#!/usr/bin/env python3
"""
Extract discourse nodes and relations from papers CSV using Claude API.
Works with Title and Abstract columns only.

Usage: python3 extract-claims-evidence-from-abstracts.py <csv_path> <focal_question> <node_type1> [<node_type2> ...]
Example: python3 extract-claims-evidence-from-abstracts.py papers.csv "My question" Evidence Claim Question
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


def load_schema():
    """Load the discourse graph schema."""
    schema_path = '.obsidian/plugins/discourse-graphs/data.json'
    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)

    with open(schema_path, 'r') as f:
        return json.load(f)


def build_config_from_node_types(schema, requested_node_types):
    """Build extraction config from requested node type names."""
    # Filter node types by name
    selected_node_types = [
        nt for nt in schema['nodeTypes']
        if nt['name'] in requested_node_types
    ]

    if not selected_node_types:
        print(f"Error: None of the requested node types found in schema")
        print(f"Requested: {', '.join(requested_node_types)}")
        print(f"Available: {', '.join([nt['name'] for nt in schema['nodeTypes']])}")
        sys.exit(1)

    # Get node type IDs for filtering discourse relations
    selected_node_type_ids = {nt['id'] for nt in selected_node_types}

    # Filter discourse relations to only include those between selected node types
    filtered_discourse_relations = [
        dr for dr in schema['discourseRelations']
        if dr['sourceId'] in selected_node_type_ids and dr['destinationId'] in selected_node_type_ids
    ]

    config = {
        'nodeTypes': selected_node_types,
        'relationTypes': schema['relationTypes'],
        'discourseRelations': filtered_discourse_relations
    }

    return config


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


def generate_question_abbreviation(question, max_keywords=5):
    """Generate an abbreviated filename from a research question."""
    # Common stop words to remove
    stop_words = {
        'how', 'what', 'why', 'when', 'where', 'who', 'which', 'whose',
        'are', 'is', 'was', 'were', 'be', 'been', 'being',
        'the', 'a', 'an', 'and', 'or', 'but', 'for', 'at', 'by', 'from',
        'to', 'in', 'on', 'of', 'with', 'as', 'do', 'does', 'did',
        'have', 'has', 'had', 'can', 'could', 'will', 'would', 'should',
        'may', 'might', 'must', 'that', 'this', 'these', 'those'
    }

    # Remove punctuation and convert to lowercase
    cleaned = re.sub(r'[^\w\s]', '', question.lower())

    # Split into words and filter stop words
    words = [w for w in cleaned.split() if w and w not in stop_words]

    # Take up to max_keywords
    keywords = words[:max_keywords]

    # If we got no keywords, use a default
    if not keywords:
        return "synthesis"

    # Join with hyphens
    return '-'.join(keywords)


def extract_nodes_from_paper(client, paper_data, research_question, config):
    """
    Use Claude API to extract discourse nodes from a single paper.
    Returns a dict mapping node types to lists of extracted nodes.
    """
    # Build context from paper fields
    title = paper_data.get('Title', paper_data.get('title', 'Unknown'))
    authors = paper_data.get('Authors', paper_data.get('authors', 'Unknown'))
    year = paper_data.get('Year', paper_data.get('year', 'Unknown'))

    paper_context = f"""
        Paper: {title}
        Authors: {authors}
        Year: {year}

        Research Question Context: {research_question}

        """

    # Use Abstract if available, otherwise use substantive fields
    abstract = paper_data.get('Abstract', paper_data.get('abstract', ''))
    if abstract and not pd.isna(abstract):
        paper_context += f"Abstract:\n{abstract}\n"
    else:
        # Use substantive fields instead
        paper_context += "Paper Content (from substantive fields):\n\n"

        # List of common substantive field patterns
        substantive_fields = []
        for col in paper_data.index:
            # Skip metadata and supporting fields
            if any(skip in col.lower() for skip in ['doi', 'link', 'venue', 'citation', 'supporting', 'reasoning']):
                continue
            if not pd.isna(paper_data[col]) and str(paper_data[col]).strip():
                substantive_fields.append((col, paper_data[col]))

        if substantive_fields:
            for field_name, field_value in substantive_fields:
                paper_context += f"## {field_name}\n{field_value}\n\n"
        else:
            paper_context += "(No detailed content available)\n"

    # Build node type descriptions for the prompt
    node_type_descriptions = []
    for node_type in config['nodeTypes']:
        node_type_descriptions.append(
            f"- **{node_type['name']}**: {node_type.get('description', 'No description')}"
        )

    node_types_text = "\n".join(node_type_descriptions)

    prompt = f"""Given the following paper abstract, extract discourse nodes of the specified types.

{paper_context}

Node Types to Extract:
{node_types_text}

For each node type, relevant items from the abstract if it is present. Return your response as a JSON object
where keys are node type names and values are arrays of extracted items.

For Evidence nodes, include What/How/Who methodological notes:
{{
  "Evidence": [
    {{
      "content": "The main evidence statement",
      "what": "What was measured/collected",
      "how": "How it was measured/analyzed",
      "who": "Who/what dataset was used"
    }}
  ],
  "Claim": [
    {{
      "content": "A generalized assertion from the paper"
    }}
  ],
  "Question": [
    {{
      "content": "A research question addressed or raised"
    }}
  ]
}}

IMPORTANT:
- Extract actual content from the paper data, not placeholder text
- Be specific and concrete
- For Evidence: Focus on empirical findings with methodological details
- For Claims: Extract generalizable assertions
- For Questions: Extract research questions addressed or raised
- For Patterns: Extract higher level conceptual design patterns or working principles that enable a specific Artifact's key functions
- For Artifacts: Extract specific tools, systems, or techniques introduced or studied in the paper
- Only include items that are clearly supported by the paper content
- Return an empty array for node types with no relevant content
- Note "Details not specified" when methodological details are unclear
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
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            extracted_nodes = json.loads(json_match.group(0))
            return extracted_nodes
        else:
            print(f"Warning: Could not parse JSON from response for {title}")
            return {}

    except Exception as e:
        print(f"Error extracting nodes from {title}: {e}")
        return {}


def identify_relations_between_nodes(client, extracted_nodes, config):
    """
    Use Claude API to identify relationships between extracted nodes.
    Returns a list of relations with source, target, and relation type.
    """
    # Build a summary of all extracted nodes with IDs
    nodes_summary = []
    node_id_map = {}
    current_id = 0

    for node_type_name, nodes in extracted_nodes.items():
        # Skip if nodes is None or empty
        if not nodes:
            continue

        for idx, node in enumerate(nodes):
            node_id = f"{node_type_name.lower()}-{current_id:03d}"
            node_id_map[node_id] = {
                'type': node_type_name,
                'content': node['content'],
                'index': idx
            }
            nodes_summary.append(f"[{node_id}] ({node_type_name}) {node['content']}")
            current_id += 1

    # If there are fewer than 2 nodes, no relations possible
    if len(nodes_summary) < 2:
        return []

    nodes_text = "\n".join(nodes_summary)

    # Build relation type descriptions
    relation_descriptions = []
    for rel_type in config['relationTypes']:
        relation_descriptions.append(
            f"- **{rel_type['label']}**: {rel_type.get('complement', '')}"
        )

    relations_text = "\n".join(relation_descriptions)

    # Get valid discourse relations from schema
    valid_relations_text = "Valid node-to-node relation patterns:\n"
    node_type_id_map = {nt['id']: nt['name'] for nt in config['nodeTypes']}
    rel_type_id_map = {rt['id']: rt['label'] for rt in config['relationTypes']}

    for disc_rel in config['discourseRelations']:
        source_name = node_type_id_map.get(disc_rel['sourceId'], 'Unknown')
        target_name = node_type_id_map.get(disc_rel['destinationId'], 'Unknown')
        rel_label = rel_type_id_map.get(disc_rel['relationshipTypeId'], 'Unknown')
        valid_relations_text += f"- {source_name} {rel_label} {target_name}\n"

    prompt = f"""Given the following extracted discourse nodes, identify relationships between them.

Extracted Nodes:
{nodes_text}

Relation Types Available:
{relations_text}

{valid_relations_text}

For each meaningful relationship you identify, return a JSON array with:
{{
  "source_id": "the source node ID (e.g., 'evidence-001')",
  "target_id": "the target node ID (e.g., 'claim-005')",
  "relation_type": "the relation label (e.g., 'supports', 'opposes')"
}}

IMPORTANT:
- Only identify relationships that are explicitly or strongly implied in the content
- Follow the valid node-to-node relation patterns provided above
- Focus on the most important and clear relationships
- Return an empty array if no clear relationships exist

Return as a JSON array:
[
  {{"source_id": "evidence-001", "target_id": "claim-002", "relation_type": "supports"}},
  ...
]
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

        response_text = response.content[0].text

        # Extract JSON array
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            relations = json.loads(json_match.group(0))
            # Validate and enrich relations
            valid_relations = []
            for rel in relations:
                if rel['source_id'] in node_id_map and rel['target_id'] in node_id_map:
                    rel['source_node'] = node_id_map[rel['source_id']]
                    rel['target_node'] = node_id_map[rel['target_id']]
                    valid_relations.append(rel)
            return valid_relations
        else:
            return []

    except Exception as e:
        print(f"Error identifying relations: {e}")
        return []


def generate_paper_markdown(paper_data, extracted_nodes, relations, filename, evidence_dir, config):
    """Generate markdown file for a single paper with extracted nodes and relations."""
    title = paper_data.get('Title', paper_data.get('title', 'Unknown'))
    authors = paper_data.get('Authors', paper_data.get('authors', 'Unknown'))
    year = paper_data.get('Year', paper_data.get('year', 'Unknown'))
    doi = paper_data.get('DOI', paper_data.get('doi', 'N/A'))
    citation_count = paper_data.get('Citation count', paper_data.get('citation_count', 'N/A'))

    content = f"""# {title}

**Authors:** {authors}
**Year:** {year}
**DOI:** {doi}
**Citation Count:** {citation_count}

"""

    # Get node type info for tags
    node_type_tags = {nt['name']: nt.get('tag', '') for nt in config['nodeTypes']}

    # Organize nodes by type
    for node_type_name, nodes in extracted_nodes.items():
        if not nodes:
            continue

        content += f"## {node_type_name} Items\n\n"

        tag = node_type_tags.get(node_type_name, '')
        tag_str = f" #{tag}" if tag else ""

        for idx, node in enumerate(nodes):
            node_id = f"{node_type_name.lower()}-{idx:03d}"

            # Check if this is an Evidence node with What/How/Who
            if node_type_name == "Evidence" and all(k in node for k in ['what', 'how', 'who']):
                content += f"""- {node['content']}{tag_str} ^{node_id}
\t- **What**: {node['what']}
\t- **How**: {node['how']}
\t- **Who**: {node['who']}
"""
            else:
                content += f"- {node['content']}{tag_str} ^{node_id}\n"

        content += "\n"

    # Add relations section if any
    if relations:
        content += "## Identified Relations\n\n"
        for rel in relations:
            source = rel['source_node']
            target = rel['target_node']
            rel_type = rel['relation_type']
            content += f"- {source['type']} '{source['content'][:50]}...' **{rel_type}** {target['type']} '{target['content'][:50]}...'\n"

    # Write to file
    filepath = os.path.join(evidence_dir, filename + ".md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created {filepath}")

    return filepath


def synthesize_across_papers(client, all_paper_data, research_question, config):
    """
    Use Claude API to synthesize higher-level nodes across all papers.
    Returns dict with 'patterns' and 'claims' keys.
    """
    # Build summary of all extracted nodes
    summary = "# All Extracted Nodes Across Papers\n\n"

    for paper_file, paper_title, extracted_nodes in all_paper_data:
        summary += f"\n## From: {paper_title} ({paper_file})\n\n"
        for node_type_name, nodes in extracted_nodes.items():
            if nodes:
                summary += f"### {node_type_name}:\n"
                for idx, node in enumerate(nodes):
                    node_id = f"{node_type_name.lower()}-{idx:03d}"
                    summary += f"- [{node_id}] {node['content']}\n"
                summary += "\n"

    result = {'patterns': [], 'claims': []}

    # First, identify cross-paper patterns
    print("  Identifying cross-paper patterns...")
    patterns_prompt = f"""
        Given the following nodes extracted from multiple research papers,
        identify 3-10 recurring patterns that appear across papers.

        Research Question: {research_question}

        {summary}

        For each pattern, identify which Artifact uses/instantiates it, and what Claims or Evidence relate to it.

        Return as a JSON array where each item has:
        {{
        "pattern": "Description of the pattern (e.g., 'Mixture of Experts', 'Chain of Thought prompting', 'Ephemeral UIs')",
        "supporting_nodes": [
            {{"paper_file": "@filename.md", "node_type": "Evidence", "node_id": "evidence-001"}},
            {{"paper_file": "@filename.md", "node_type": "Claim", "node_id": "claim-002"}}
            {{"paper_file": "@filename.md", "node_type": "Artifact", "node_id": "art-002"}}
        ]
        }}

        Focus on patterns that:
        - Appear in multiple papers (2+)
        - Help answer the research question
        - Can be mapped to Artifacts, Claims, or Evidence from the papers

        Each pattern should be supported by nodes from at least 2 different papers.
        """

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": patterns_prompt
            }]
        )

        response_text = response.content[0].text
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            result['patterns'] = json.loads(json_match.group(0))
            print(f"  Identified {len(result['patterns'])} patterns")
        else:
            print("  Warning: Could not parse patterns from response")

    except Exception as e:
        print(f"  Error identifying patterns: {e}")

    # Then, synthesize high-level claims
    claim_node_type = next((nt for nt in config['nodeTypes'] if nt['name'] == 'Claim'), None)

    if claim_node_type:
        print("  Synthesizing high-level claims...")
        claims_prompt = f"""
        Given the following nodes extracted from multiple research papers,
        synthesize 5-15 high-level candidate Claims that address the research question.

        Research Question: {research_question}

        {summary}

        For each synthesized claim, identify which nodes from the papers support it.

        Return as a JSON array where each item has:
        {{
        "claim": "The synthesized claim statement",
        "supporting_nodes": [
            {{"paper_file": "@filename.md", "node_type": "Evidence", "node_id": "evidence-001"}},
            {{"paper_file": "@filename.md", "node_type": "Claim", "node_id": "claim-002"}}
        ]
        }}

        Generate claims that:
        - Synthesize findings at a higher level of abstraction
        - Address the research question directly
        - Are supported by evidence from the papers
        - Make generalizable assertions

        Each claim should be supported by at least one node from the papers.
        """

        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                messages=[{
                    "role": "user",
                    "content": claims_prompt
                }]
            )

            response_text = response.content[0].text
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                result['claims'] = json.loads(json_match.group(0))
                print(f"  Synthesized {len(result['claims'])} claims")
            else:
                print("  Warning: Could not parse claims from response")

        except Exception as e:
            print(f"  Error synthesizing claims: {e}")
    else:
        print("  Skipping claim synthesis (Claim node type not selected)")

    return result


def generate_synthesis_markdown(synthesis_data, research_question, claims_dir, config):
    """Generate the synthesis markdown file with cross-paper patterns and claims."""

    claim_tag = next((nt.get('tag', '') for nt in config['nodeTypes'] if nt['name'] == 'Claim'), 'clm-candidate')

    # Generate abbreviated filename from research question
    question_abbrev = generate_question_abbreviation(research_question)
    filename = f"synthesis-{question_abbrev}.md"

    content = f"""
    # Cross-Paper Synthesis

    Research Question: {research_question}

    """

    # Add patterns section if any
    if synthesis_data.get('patterns'):
        content += f"""
        ## Patterns

        Cross-paper patterns and themes identified across the literature:

        """
        for pattern_data in synthesis_data['patterns']:
            pattern = pattern_data['pattern']

            # Build links to supporting nodes
            support_links = []
            for support in pattern_data.get('supporting_nodes', []):
                paper_file = support['paper_file']
                node_id = support['node_id']
                support_links.append(f"[[{paper_file}]]-node_id")

            links_str = " ".join(support_links)
            content += f"- **{pattern}** {links_str}\n"

        content += "\n"

    # Add claims section if any
    if synthesis_data.get('claims'):
        content += f"""
        ## Synthesized Claims

        High-level claims synthesized across papers:

        """
        for claim_data in synthesis_data['claims']:
            claim = claim_data['claim']

            # Build links to supporting nodes
            support_links = []
            for support in claim_data.get('supporting_nodes', []):
                paper_file = support['paper_file']
                node_id = support['node_id']
                support_links.append(f"[[{paper_file}]]-node_id")

            links_str = " ".join(support_links)
            tag_str = f" #{claim_tag}" if claim_tag else ""
            content += f"- {claim}{tag_str} {links_str}\n"

    # Write to file
    filepath = os.path.join(claims_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nCreated {filepath}")
    return filename


def main():
    """Main extraction workflow."""

    if len(sys.argv) < 4:
        print("Usage: python3 extract-claims-evidence-from-abstracts.py <csv_path> <focal_question> <node_type1> [<node_type2> ...]")
        print("Example: python3 extract-claims-evidence-from-abstracts.py papers.csv \"My question\" Evidence Claim Question")
        sys.exit(1)

    csv_path = sys.argv[1]
    research_question = sys.argv[2]
    requested_node_types = sys.argv[3:]  # All remaining args are node type names

    print("Starting discourse node extraction...")
    print(f"Research Question: {research_question}")
    print(f"Requested node types: {', '.join(requested_node_types)}\n")

    # Load schema and build configuration
    schema = load_schema()
    config = build_config_from_node_types(schema, requested_node_types)
    print(f"Extracting {len(config['nodeTypes'])} node types with {len(config['discourseRelations'])} possible discourse relations\n")

    # Initialize Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    # Create directories if they don't exist
    evidence_dir = "evidence"
    claims_dir = "claims"
    os.makedirs(evidence_dir, exist_ok=True)
    os.makedirs(claims_dir, exist_ok=True)

    # Load CSV
    print(f"Loading CSV from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} papers\n")

    # Check for required columns (case-insensitive)
    columns_lower = [col.lower() for col in df.columns]
    if 'title' not in columns_lower:
        print("Error: CSV must contain 'Title' column")
        print(f"Found columns: {', '.join(df.columns)}")
        sys.exit(1)

    # Standardize column names
    df.columns = [col.lower().capitalize() if col.lower() in ['title', 'abstract', 'authors', 'year', 'doi'] else col for col in df.columns]

    # Check if we have Abstract column or need to use substantive fields
    has_abstract = 'Abstract' in df.columns or 'abstract' in [col.lower() for col in df.columns]
    if not has_abstract:
        print("Note: No 'Abstract' column found. Will use substantive fields for extraction.\n")

    # Process each paper
    all_paper_data = []

    for idx, row in df.iterrows():
        title = row.get('Title', row.get('title', 'Unknown'))
        print(f"\n[{idx + 1}/{len(df)}] Processing: {title[:60]}...")

        # Extract nodes
        extracted_nodes = extract_nodes_from_paper(client, row, research_question, config)

        if not extracted_nodes:
            print(f"  No nodes extracted, skipping...")
            continue

        # Count total nodes (handle empty/None values)
        total_nodes = sum(len(nodes) for nodes in extracted_nodes.values() if nodes)
        node_types_with_content = len([nodes for nodes in extracted_nodes.values() if nodes])
        print(f"  Extracted {total_nodes} nodes across {node_types_with_content} types")

        # Identify relations between nodes
        print(f"  Identifying relations...")
        relations = identify_relations_between_nodes(client, extracted_nodes, config)
        print(f"  Identified {len(relations)} relations")

        # Generate filename
        authors = row.get('Authors', row.get('authors', ''))
        year = row.get('Year', row.get('year', 'unknown'))
        filename = sanitize_author_year(authors, year)

        # Generate paper markdown
        generate_paper_markdown(row, extracted_nodes, relations, filename, evidence_dir, config)

        # Store for synthesis
        all_paper_data.append((filename + ".md", title, extracted_nodes))

    print(f"\n\nGenerated {len(all_paper_data)} paper files")

    # Synthesize across papers
    synthesis_filename = None
    if len(all_paper_data) > 1:
        print("\n" + "="*60)
        print("Synthesizing across all papers...")
        print("="*60 + "\n")

        synthesis_data = synthesize_across_papers(client, all_paper_data, research_question, config)

        # Generate synthesis markdown
        synthesis_filename = generate_synthesis_markdown(synthesis_data, research_question, claims_dir, config)

    print("\n" + "="*60)
    print("Extraction complete!")
    print("="*60)
    print(f"\nOutput:")
    print(f"  - Paper files: {evidence_dir}/ ({len(all_paper_data)} files)")
    if synthesis_filename:
        print(f"  - Synthesis file: {claims_dir}/{synthesis_filename}")


if __name__ == "__main__":
    main()
