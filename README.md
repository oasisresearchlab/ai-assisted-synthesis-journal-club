# ai-assisted-synthesis-journal-club
Prototyping an AI-assisted synthesis journal club

## Overview

General flow:
1. Define research question
2. Collect relevant papers. This can be sped up with AI tools like Elicit to get a first pass at relevant papers. Getting this into the repo is a manual step for now, into a csv. Later we can automate this more with APIs like [Asta](https://allenai.org/asta/resources/mcp).
3. Extract candidate discourse nodes (claims, evidence, patterns, artifacts) from paper abstracts that might be relevant to the research question. Current script: `scripts/extract-claims-evidence-from-abstracts.py` - this uses an LLM to extract relevant nodes from abstracts based on predefined node types, that are defined by the user with the [Discourse Graph plugin](https://discoursegraphs.com/docs/obsidian/getting-started) for Obsidian, stored in `.obsidian/plugins/discourse-graph/data.json`.
4. Verify and formalized candidate nodes. This is currently a primarily manual step, using the Discourse Graph plugin UI. There is some experimental support for using LLMs to help verify and formalize claims via API connections to a local Zotero library, see `scripts/verify-and-formalize-claims.py`.
5. Synthesize high-level claims and patterns across papers. This is the journal club step! :) The idea is for participants to do step 3 and 4 for a set of papers, then bring the resulting nodes to a synthesis journal club where they can discuss and collaboratively synthesize high-level claims and patterns across papers, e.g., using the Discourse Graph plugin canvas.

See more plans in `plan.md`

## Setup

### Prerequisites

1. **Obsidian** with the following plugins:
   - [Discourse Graphs](https://discoursegraphs.com/docs/obsidian/getting-started) - for schema and node management
   - Claims & Evidence Extractor (included in `.obsidian/plugins/`)

2. **Python 3** with dependencies:
   ```bash
   pip install anthropic pandas python-dotenv
   ```

3. **Anthropic API Key** - Create a `.env` file in the vault root:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

## Using the Claims & Evidence Extractor

The extractor plugin provides a GUI for batch-extracting discourse nodes from paper abstracts.

### Step 1: Prepare Your CSV

Export papers from your literature search tool (Elicit, Semantic Scholar, etc.) as CSV. Required columns:
- `Title` - paper title
- `Abstract` - paper abstract

Optional columns: `Authors`, `Year`, `DOI`, `Citation count`

### Step 2: Open the Extractor

Either:
- Click the **brain icon** in the left ribbon
- Use command palette: `Extract Claims & Evidence from CSV`

### Step 3: Configure Extraction

1. **CSV File**: Browse to select your CSV file
2. **Focal Question**: Enter your research question to guide extraction
3. **Node Types**: Toggle which types to extract (Evidence, Claims, Questions, etc.). Available node types are drawn from the Discourse Graph schema defined in the Discourse Graphs plugin.
4. **Relations**: Toggle which relationships to identify (supports, opposes, informs). Available relation types are drawn from the Discourse Graph schema defined in the Discourse Graphs plugin.

### Step 4: Run Extraction

Click **Extract**. The plugin will:
1. Process each paper through Claude API
2. Extract evidence items with What/How/Who methodology notes
3. Generate markdown files in `evidence/` folder
4. Synthesize cross-paper claims in `claims/` folder

### Output Structure

```
evidence/
  @smith-2024.md      # One file per paper
  @jones-2023.md
claims/
  central-claims.md   # Synthesized claims with evidence links
```

Each evidence file contains:
```markdown
# Paper Title

**Authors:** ...
**Year:** ...

## Evidence Items

- Finding statement #evd-candidate ^evd-001
    - **What**: Measures/data collected
    - **How**: Methods used
    - **Who**: Participants/dataset
```

### Next Steps

After extraction:
1. Review candidate nodes (tagged `#evd-candidate`, `#clm-candidate`)
2. Use Discourse Graphs plugin to promote verified candidates to formal nodes
3. Build synthesis on the Discourse Graph canvas