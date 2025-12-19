const { Plugin, Modal, Notice, Setting } = require('obsidian');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

class ExtractionModal extends Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
    this.csvPath = '';
    this.focalQuestion = '';
    this.selectedNodeTypes = new Set();
    this.selectedRelationTypes = new Set();
    this.schema = null;
    this.loadSchema();
  }

  loadSchema() {
    try {
      const schemaPath = path.join(
        this.app.vault.adapter.basePath,
        '.obsidian/plugins/discourse-graphs/data.json'
      );
      if (fs.existsSync(schemaPath)) {
        const schemaData = fs.readFileSync(schemaPath, 'utf-8');
        this.schema = JSON.parse(schemaData);

        // Create lookup maps for dereferencing IDs
        this.nodeTypeMap = {};
        this.relationTypeMap = {};

        this.schema.nodeTypes.forEach(nt => {
          this.nodeTypeMap[nt.id] = nt;
        });

        this.schema.relationTypes.forEach(rt => {
          this.relationTypeMap[rt.id] = rt;
        });

        // Default selections: all node types except Source
        this.schema.nodeTypes.forEach(nodeType => {
          if (nodeType.name !== 'Source') {
            this.selectedNodeTypes.add(nodeType.id);
          }
        });

        // Default selections: all discourse relations
        this.schema.discourseRelations.forEach((discRel, idx) => {
          this.selectedRelationTypes.add(idx);
        });
      }
    } catch (error) {
      console.error('Error loading discourse graph schema:', error);
    }
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass('extraction-modal');

    contentEl.createEl('h2', { text: 'Extract Discourse Nodes & Relations' });

    // Create a container for all settings
    const settingsContainer = contentEl.createDiv({ cls: 'settings-container' });

    // CSV File Picker
    new Setting(settingsContainer)
      .setName('CSV File')
      .setDesc('Select a CSV file containing papers (requires Title; uses Abstract, Abstract Note, or other content columns)')
      .addText(text => {
        text.setPlaceholder('Path to CSV file')
          .setValue(this.csvPath)
          .onChange(value => {
            this.csvPath = value;
          });
        text.inputEl.style.width = '100%';
      })
      .addButton(button => {
        button
          .setButtonText('Browse')
          .onClick(async () => {
            const electron = require('electron');
            const result = await electron.remote.dialog.showOpenDialog({
              properties: ['openFile'],
              filters: [
                { name: 'CSV Files', extensions: ['csv'] }
              ]
            });

            if (!result.canceled && result.filePaths.length > 0) {
              this.csvPath = result.filePaths[0];
              // Update the text input
              const textInput = settingsContainer.querySelector('input[type="text"]');
              if (textInput) {
                textInput.value = this.csvPath;
              }
            }
          });
      });

    // Focal Question Input
    new Setting(settingsContainer)
      .setName('Focal Question')
      .setDesc('Enter your research question')
      .addTextArea(text => {
        text.setPlaceholder('e.g., How effective are AI systems at claim verification?')
          .setValue(this.focalQuestion)
          .onChange(value => {
            this.focalQuestion = value;
          });
        text.inputEl.rows = 4;
        text.inputEl.style.width = '100%';
      });

    // Node Types Section
    if (this.schema && this.schema.nodeTypes) {
      settingsContainer.createEl('h3', { text: 'Node Types to Extract' });
      settingsContainer.createEl('p', {
        text: 'Select which types of discourse nodes to extract from papers:',
        cls: 'setting-item-description'
      });

      const nodeTypesContainer = settingsContainer.createDiv({ cls: 'node-selection-container' });

      this.schema.nodeTypes.forEach(nodeType => {
        if (nodeType.name === 'Source') return; // Skip Source type

        const checkboxSetting = new Setting(nodeTypesContainer)
          .setName(nodeType.name)
          .setDesc(nodeType.description || '');

        checkboxSetting.addToggle(toggle => {
          toggle
            .setValue(this.selectedNodeTypes.has(nodeType.id))
            .onChange(value => {
              if (value) {
                this.selectedNodeTypes.add(nodeType.id);
              } else {
                this.selectedNodeTypes.delete(nodeType.id);
              }
            });
        });

        // Add color indicator
        const nameEl = checkboxSetting.nameEl;
        const colorDot = nameEl.createSpan({ cls: 'node-type-color' });
        colorDot.style.backgroundColor = nodeType.color;
        nameEl.prepend(colorDot);
      });
    }

    // Discourse Relations Section
    if (this.schema && this.schema.discourseRelations) {
      settingsContainer.createEl('h3', { text: 'Discourse Relations to Identify' });
      settingsContainer.createEl('p', {
        text: 'Select which relationships to identify between nodes:',
        cls: 'setting-item-description'
      });

      const relationTypesContainer = settingsContainer.createDiv({ cls: 'node-selection-container' });

      this.schema.discourseRelations.forEach((discRel, idx) => {
        // Dereference IDs to build label
        const sourceNode = this.nodeTypeMap[discRel.sourceId];
        const targetNode = this.nodeTypeMap[discRel.destinationId];
        const relationType = this.relationTypeMap[discRel.relationshipTypeId];

        if (!sourceNode || !targetNode || !relationType) {
          return; // Skip if any lookup fails
        }

        const label = `${sourceNode.name} ${relationType.label} ${targetNode.name}`;

        const checkboxSetting = new Setting(relationTypesContainer)
          .setName(label);

        checkboxSetting.addToggle(toggle => {
          toggle
            .setValue(this.selectedRelationTypes.has(idx))
            .onChange(value => {
              if (value) {
                this.selectedRelationTypes.add(idx);
              } else {
                this.selectedRelationTypes.delete(idx);
              }
            });
        });

        // Add color indicator from relation type
        const nameEl = checkboxSetting.nameEl;
        const colorDot = nameEl.createSpan({ cls: 'relation-type-color' });
        colorDot.style.backgroundColor = relationType.color;
        nameEl.prepend(colorDot);
      });
    }

    // Action Buttons
    const buttonContainer = contentEl.createDiv({ cls: 'modal-button-container' });
    buttonContainer.style.display = 'flex';
    buttonContainer.style.justifyContent = 'flex-end';
    buttonContainer.style.gap = '10px';
    buttonContainer.style.marginTop = '20px';

    const cancelButton = buttonContainer.createEl('button', { text: 'Cancel' });
    cancelButton.addEventListener('click', () => {
      this.close();
    });

    const runButton = buttonContainer.createEl('button', {
      text: 'Extract',
      cls: 'mod-cta'
    });
    runButton.addEventListener('click', () => {
      this.runExtraction();
    });
  }

  async runExtraction() {
    if (!this.csvPath) {
      new Notice('Please select a CSV file');
      return;
    }

    if (!this.focalQuestion) {
      new Notice('Please enter a focal question');
      return;
    }

    if (this.selectedNodeTypes.size === 0) {
      new Notice('Please select at least one node type to extract');
      return;
    }

    // Validate CSV file exists
    if (!fs.existsSync(this.csvPath)) {
      new Notice('CSV file not found: ' + this.csvPath);
      return;
    }

    this.close();

    // Show progress notice
    new Notice('Starting extraction... This may take several minutes.');

    // Get vault path
    const vaultPath = this.app.vault.adapter.basePath;

    // Path to the Python script
    const scriptPath = path.join(vaultPath, 'scripts', 'extract-claims-evidence-from-abstracts.py');

    // Check if script exists, if not create it
    if (!fs.existsSync(scriptPath)) {
      new Notice('Creating extraction script...');
      await this.plugin.createExtractionScript(scriptPath);
    }

    // Prepare configuration with selected node types and discourse relations
    const config = {
      nodeTypes: this.schema ? this.schema.nodeTypes.filter(nt =>
        this.selectedNodeTypes.has(nt.id)
      ) : [],
      relationTypes: this.schema ? this.schema.relationTypes : [],
      discourseRelations: this.schema ? this.schema.discourseRelations.filter((dr, idx) =>
        this.selectedRelationTypes.has(idx)
      ) : []
    };

    // Write config to temporary file
    const configPath = path.join(vaultPath, '.extraction-config.json');
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

    // Construct command with config file
    const command = `cd "${vaultPath}" && python3 "${scriptPath}" "${this.csvPath}" "${this.focalQuestion.replace(/"/g, '\\"')}" "${configPath}"`;

    // Execute Python script
    exec(command, { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
      // Clean up config file
      try {
        fs.unlinkSync(configPath);
      } catch (e) {
        console.warn('Could not delete temporary config file:', e);
      }

      if (error) {
        console.error('Extraction error:', error);
        console.error('stderr:', stderr);
        new Notice('Error during extraction: ' + error.message);
        return;
      }

      if (stderr) {
        console.log('stderr:', stderr);
      }

      console.log('stdout:', stdout);
      new Notice('Extraction complete! Check the evidence/ and claims/ folders.');
    });
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

class ClaimsEvidenceExtractorPlugin extends Plugin {
  async onload() {
    console.log('Loading Claims & Evidence Extractor plugin');

    // Add command to open extraction modal
    this.addCommand({
      id: 'open-extraction-modal',
      name: 'Extract Claims & Evidence from CSV',
      callback: () => {
        new ExtractionModal(this.app, this).open();
      }
    });

    // Add ribbon icon
    this.addRibbonIcon('brain', 'Extract Claims & Evidence', () => {
      new ExtractionModal(this.app, this).open();
    });
  }

  async createExtractionScript(scriptPath) {
    const scriptContent = `#!/usr/bin/env python3
"""
Extract claims and evidence from papers CSV using Claude API.
Requires Title column; uses Abstract, Abstract Note (Zotero), or falls back to
content columns like Reasoning for.../Supporting... (Elicit).

Usage: python3 extract-claims-evidence-from-abstracts.py <csv_path> <focal_question>
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


def generate_citekey(authors, title, year):
    """
    Generate citation key using BetterBibTeX-style formula: auth.lower+shorttitle(3,3)+year
    Example: Greene et al "Better, Nicer, Clearer, Fairer: A Critical Assessment..." (2019)
             -> greeneBetterNicerClearer2019
    """
    # Get author part (lowercase)
    if pd.isna(authors) or not authors:
        auth_part = "unknown"
    else:
        first_author = authors.split(',')[0].strip()
        if ',' in first_author:
            last_name = first_author.split(',')[0].strip()
        else:
            parts = first_author.split()
            last_name = parts[-1] if parts else "unknown"
        auth_part = re.sub(r'[^a-zA-Z]', '', last_name).lower()

    # Get shorttitle part (first 3 non-stopword words, CamelCased)
    if pd.isna(title) or not title:
        title_part = ""
    else:
        stopwords = {'a', 'an', 'the', 'of', 'and', 'or', 'for', 'to', 'in', 'on', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'but', 'if', 'while', 'although', 'though', 'because', 'since', 'unless', 'so', 'that', 'than', 'whether', 'as', 'what', 'which', 'who', 'whom', 'whose', 'when', 'where', 'why', 'how'}
        words = re.findall(r'[a-zA-Z]+', title)
        meaningful_words = [w for w in words if w.lower() not in stopwords][:3]
        title_part = ''.join(w.capitalize() for w in meaningful_words)

    # Get year part
    year_part = str(year) if year and not pd.isna(year) else ""

    return f"@{auth_part}{title_part}{year_part}"


def extract_evidence_from_paper(client, paper_data, research_question):
    """
    Use Claude API to extract evidence items from a single paper.
    Returns a list of evidence items with What/How/Who notes.
    """
    # Build context from paper fields
    title = paper_data.get('Title', paper_data.get('title', 'Unknown'))
    abstract = paper_data.get('Abstract', paper_data.get('abstract', ''))
    authors = paper_data.get('Authors', paper_data.get('authors', 'Unknown'))
    year = paper_data.get('Year', paper_data.get('year', 'Unknown'))

    paper_context = f"""
Paper: {title}
Authors: {authors}
Year: {year}

Research Question Context: {research_question}

Abstract:
{abstract}
"""

    prompt = f"""Given the following paper abstract, extract 3-8 discrete empirical evidence items
that address the research question.

{paper_context}

For each evidence item, provide:
1. A clear statement of the empirical finding/result
2. Three subbullet notes organized as:
   - **What**: Observable measures/data collected (e.g., accuracy metrics, performance scores)
   - **How**: Procedures/analyses/experimental design (e.g., methods, evaluation approaches)
   - **Who**: Participants/dataset/population (e.g., dataset details, sample characteristics)

Return your response as a JSON array where each item has:
{{
  "evidence": "The main evidence statement",
  "what": "What was measured/collected",
  "how": "How it was measured/analyzed",
  "who": "Who/what dataset was used"
}}

NOTE: Since you only have access to the abstract, some details may be limited. Extract what you can
and note "Not specified in abstract" when methodological details are unclear. Focus on the key findings
and whatever methodological details are available.
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
        json_match = re.search(r'\\[.*\\]', response_text, re.DOTALL)
        if json_match:
            evidence_items = json.loads(json_match.group(0))
            return evidence_items
        else:
            print(f"Warning: Could not parse JSON from response for {title}")
            return []

    except Exception as e:
        print(f"Error extracting evidence from {title}: {e}")
        return []


def generate_paper_markdown(paper_data, evidence_items, filename, evidence_dir):
    """Generate markdown file for a single paper with evidence items."""
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
    filepath = os.path.join(evidence_dir, filename + ".md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created {filepath}")

    return filepath


def synthesize_claims(client, all_evidence_data, research_question):
    """
    Use Claude API to synthesize claims across all evidence.
    Returns a list of claims with links to supporting evidence.
    """

    # Build evidence summary for claim synthesis
    evidence_summary = "# All Extracted Evidence\\n\\n"

    for paper_file, paper_title, evidence_items in all_evidence_data:
        evidence_summary += f"\\n## From: {paper_title} ({paper_file})\\n\\n"
        for idx, item in enumerate(evidence_items, 1):
            evidence_id = f"evd-{idx:03d}"
            evidence_summary += f"- [{evidence_id}] {item['evidence']}\\n"
            evidence_summary += f"  - What: {item['what']}\\n"
            evidence_summary += f"  - How: {item['how']}\\n"
            evidence_summary += f"  - Who: {item['who']}\\n"

    prompt = f"""Given the following evidence extracted from multiple papers,
synthesize 5-15 high-level candidate claims that address the research question.

Research Question: {research_question}

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
- Compare different approaches or systems when relevant
- Address methodological patterns when present
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
        json_match = re.search(r'\\[.*\\]', response_text, re.DOTALL)
        if json_match:
            claims = json.loads(json_match.group(0))
            return claims
        else:
            print("Warning: Could not parse claims JSON from response")
            return []

    except Exception as e:
        print(f"Error synthesizing claims: {e}")
        return []


def generate_claims_markdown(claims, research_question, claims_dir):
    """Generate the central claims markdown file."""

    content = f"""# Candidate Claims

Research Question: {research_question}

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
        content += f"- {claim} #clm-candidate {links_str}\\n"

    # Write to file
    filepath = os.path.join(claims_dir, "central-claims.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\\nCreated {filepath}")


def main():
    """Main extraction workflow."""

    if len(sys.argv) < 3:
        print("Usage: python3 extract-claims-evidence-from-abstracts.py <csv_path> <focal_question>")
        sys.exit(1)

    csv_path = sys.argv[1]
    research_question = sys.argv[2]

    print("Starting claims and evidence extraction...")
    print(f"Research Question: {research_question}\\n")

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
    print(f"Loaded {len(df)} papers\\n")

    # Check for required columns (case-insensitive)
    columns_lower = [col.lower() for col in df.columns]

    if 'title' not in columns_lower:
        print("Error: CSV must contain a 'Title' column")
        print(f"Found columns: {', '.join(df.columns)}")
        sys.exit(1)

    # Find abstract column - check variants and fallbacks
    abstract_col = None
    abstract_variants = ['abstract', 'abstract note']  # Zotero uses "Abstract Note"

    for variant in abstract_variants:
        if variant in columns_lower:
            abstract_col = df.columns[columns_lower.index(variant)]
            break

    if not abstract_col:
        # Try fallback columns by prefix (Elicit uses "Reasoning for...", "Supporting...")
        content_prefixes = ['reasoning for', 'supporting', 'summary', 'description', 'content', 'notes']
        for col, col_lower in zip(df.columns, columns_lower):
            for prefix in content_prefixes:
                if col_lower.startswith(prefix):
                    abstract_col = col
                    print(f"Note: No 'Abstract' column found, using '{abstract_col}' as content source")
                    break
            if abstract_col:
                break

    if not abstract_col:
        print("Warning: No abstract or content column found. Extraction will use title only.")
        print(f"Found columns: {', '.join(df.columns)}")
        df['Abstract'] = ''
    else:
        # Rename the found column to 'Abstract' for consistent access
        df = df.rename(columns={abstract_col: 'Abstract'})

    # Standardize other column names
    columns_lower = [col.lower() for col in df.columns]
    rename_map = {}
    for target in ['title', 'authors', 'year', 'doi']:
        if target in columns_lower and target.capitalize() not in df.columns:
            original = df.columns[columns_lower.index(target)]
            rename_map[original] = target.capitalize()
    df = df.rename(columns=rename_map)

    # Process each paper
    all_evidence_data = []

    for idx, row in df.iterrows():
        title = row.get('Title', row.get('title', 'Unknown'))
        print(f"\\n[{idx + 1}/{len(df)}] Processing: {title[:60]}...")

        # Extract evidence
        evidence_items = extract_evidence_from_paper(client, row, research_question)

        if not evidence_items:
            print(f"  No evidence extracted, skipping...")
            continue

        print(f"  Extracted {len(evidence_items)} evidence items")

        # Generate filename using BetterBibTeX-style citekey
        authors = row.get('Authors', row.get('authors', ''))
        year = row.get('Year', row.get('year', 'unknown'))
        filename = generate_citekey(authors, title, year)

        # Generate paper markdown
        generate_paper_markdown(row, evidence_items, filename, evidence_dir)

        # Store for claim synthesis
        all_evidence_data.append((filename + ".md", title, evidence_items))

    print(f"\\n\\nGenerated {len(all_evidence_data)} paper evidence files")

    # Synthesize claims
    print("\\n" + "="*60)
    print("Synthesizing claims across all evidence...")
    print("="*60 + "\\n")

    claims = synthesize_claims(client, all_evidence_data, research_question)
    print(f"Synthesized {len(claims)} candidate claims")

    # Generate claims markdown
    generate_claims_markdown(claims, research_question, claims_dir)

    print("\\n" + "="*60)
    print("Extraction complete!")
    print("="*60)
    print(f"\\nOutput:")
    print(f"  - Evidence files: {evidence_dir}/ ({len(all_evidence_data)} files)")
    print(f"  - Claims file: {claims_dir}/central-claims.md ({len(claims)} claims)")


if __name__ == "__main__":
    main()
`;

    const scriptsDir = path.dirname(scriptPath);
    if (!fs.existsSync(scriptsDir)) {
      fs.mkdirSync(scriptsDir, { recursive: true });
    }

    fs.writeFileSync(scriptPath, scriptContent);
    fs.chmodSync(scriptPath, '755');
  }

  onunload() {
    console.log('Unloading Claims & Evidence Extractor plugin');
  }
}

module.exports = ClaimsEvidenceExtractorPlugin;
