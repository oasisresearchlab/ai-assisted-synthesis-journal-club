# Claims & Evidence Extractor Plugin

An Obsidian plugin for extracting discourse nodes and relations from research papers using AI-powered analysis, integrated with the Discourse Graphs schema.

## Features

- **CSV Import**: Select a CSV file containing research papers
- **Custom Research Questions**: Define your focal research question
- **Schema-Based Extraction**: Uses your Discourse Graphs schema to extract configurable node types
- **Configurable Node Types**: Select which discourse node types to extract (Evidence, Claims, Questions, etc.)
- **Configurable Relation Types**: Select which relationship types to identify (supports, opposes, informs, enables)
- **AI-Powered Extraction**: Uses Claude AI to extract nodes and identify relationships
- **Abstract-Based Analysis**: Works with Title and Abstract columns from CSV files
- **Methodological Notes**: Extracts What/How/Who details for Evidence nodes
- **Automatic Organization**: Creates structured markdown files in evidence/ and claims/ folders
- **Cross-Paper Synthesis**: Synthesizes higher-level claims across all papers

## Setup

1. **Enable the Plugin**: Go to Settings → Community Plugins and enable "Claims & Evidence Extractor"

2. **Set Up API Key**: Ensure you have an `ANTHROPIC_API_KEY` set in your `.env` file at the vault root:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install anthropic pandas python-dotenv
   ```

## Usage

1. **Open the Extractor**:
   - Click the brain icon in the ribbon, OR
   - Use Command Palette (Ctrl/Cmd + P) → "Extract Discourse Nodes & Relations from CSV"

2. **Select Your CSV**:
   - Click "Browse" to select your CSV file
   - CSV must contain `Title` and `Abstract` columns (case-insensitive)
   - Optional columns: `Authors`, `Year`, `DOI`, `Citation count`

3. **Enter Your Research Question**:
   - Type your focal research question in the text area
   - Example: "How effective are AI systems at claim verification?"

4. **Configure Node Types**:
   - Select which discourse node types to extract from papers
   - Available types are loaded from your Discourse Graphs schema
   - Each type shows its description and color indicator
   - Default: All node types except Source are selected

5. **Configure Relation Types**:
   - Select which relationship types to identify between nodes
   - Available types are loaded from your Discourse Graphs schema
   - Each type shows its complement and color indicator
   - Default: All relation types are selected

6. **Run Extraction**:
   - Click "Extract" button
   - The process may take several minutes depending on the number of papers
   - Watch for progress notices in Obsidian

## Output

The plugin generates:

### Paper Files (`evidence/` folder)
- One markdown file per paper (e.g., `@smith-2024.md`)
- Contains extracted discourse nodes organized by type:
  - **Evidence Items**: With What/How/Who methodological notes
  - **Claims**: Generalized assertions from the paper
  - **Questions**: Research questions addressed or raised
  - Other node types as selected
- Each item tagged according to your Discourse Graphs schema
- Each item has a unique block ID for linking
- **Identified Relations**: List of relationships between nodes in the paper

### Synthesis File (`claims/synthesized-claims.md`)
- Synthesized high-level claims across all papers
- Each claim linked to supporting nodes from individual papers
- Tagged with `#clm-candidate`
- Only generated when processing multiple papers

## CSV Format

Your CSV should have these columns:

| Required | Column Name | Description |
|----------|------------|-------------|
| ✓ | Title | Paper title |
| ✓ | Abstract | Paper abstract |
| | Authors | Paper authors |
| | Year | Publication year |
| | DOI | Digital Object Identifier |
| | Citation count | Number of citations |

Column names are case-insensitive (e.g., "title", "Title", "TITLE" all work).

## Schema Integration

The plugin integrates with the Discourse Graphs plugin schema:

- **Node Types**: Loaded from `.obsidian/plugins/discourse-graphs/data.json`
- **Relation Types**: Loaded from the same schema file
- **Discourse Relations**: Valid node-to-node relationship patterns guide the AI
- **Tags**: Uses the tags defined in your schema (e.g., `#evd-candidate`, `#clm-candidate`)
- **Colors**: Displays schema-defined colors for each node and relation type

If the schema file is not found, the plugin will still work but with reduced functionality.

## Notes

- The extraction process uses Claude Sonnet 4 and requires an active API key
- Since analysis is based on abstracts, some methodological details may be limited
- The plugin will note "Not specified in abstract" when details are unclear
- Extraction quality depends on abstract completeness and detail
- Relation identification works best with clear, explicit relationships in the abstract
- Cross-paper synthesis requires at least 2 papers in the CSV

## Troubleshooting

**"CSV file not found"**: Make sure you've selected a valid CSV file path

**"ANTHROPIC_API_KEY environment variable not set"**: Check your `.env` file at vault root

**"CSV must contain 'Title' and 'Abstract' columns"**: Verify your CSV has these required columns

**No output generated**: Check the Obsidian console (Ctrl/Cmd + Shift + I) for error messages

## Technical Details

- **Platform**: Desktop only (requires Node.js child_process for Python execution)
- **Python Version**: Requires Python 3.6+
- **API Model**: Claude Sonnet 4 (claude-sonnet-4-20250514)
