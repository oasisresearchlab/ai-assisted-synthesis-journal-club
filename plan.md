# Claims and Evidence Extraction Plan

## Overview
Extract candidate claims and evidence from a CSV of papers with notes on variables for a target research question. Claims will be synthesized across papers and stored centrally, while evidence will be extracted as discrete empirical results stored in individual paper markdown files.

## File Structure

```
project-root/
├── data/
│   └── papers-llm-entailment-claim-verification.csv (existing)
├── claims/
│   └── central-claims.md (central claims document)
├── evidence/
│   ├── @paper-1-shortname.md
│   ├── @paper-2-shortname.md
│   └── ... (one file per paper, prefixed with @)
└── scripts/
    └── extract-claims-evidence.py (extraction script)
```

## Format Specifications

### Claims Format
Claims are stored in `claims/central-claims.md` as individual bullet points:

```markdown
- [Claim text synthesized across papers] #clm-candidate [[evidence/@paper-name.md#evd-001]]
```

**Example:**
```markdown
- Closed-source models (GPT-4, Claude) consistently outperform open-source models in precision and recall for claim-evidence verification tasks #clm-candidate [[evidence/@javaji-2025.md#evd-001]]
```

**Key elements:**
- Bullet point with claim text
- Tag: `#clm-candidate`
- Links to supporting evidence using block references: `[[evidence/@paper-name.md#evd-id]]`
- Note: Paper file names are prefixed with `@`

### Evidence Format
Evidence is stored in individual paper files in `evidence/` as bullet points with subbullet notes organized by What/How/Who:

```markdown
- [Evidence text with specific metrics/findings] #evd-candidate ^evd-001
	- **What**: [What observable measures/data were collected?]
	- **How**: [How were measures collected - procedures/analyses/experimental design?]
	- **Who**: [Who was data collected from - participants/dataset/population?]
```

**Example:**
```markdown
- Closed-source models (GPT-4 and Claude) outperform open-source models in precision and recall on CLAIM-BENCH dataset with over 300 claim-evidence pairs #evd-candidate ^evd-001
	- **What**: Precision and recall metrics for binary classification of claim-evidence pairs
	- **How**: Comparative evaluation using three-pass and one-by-one prompting approaches across six diverse LLMs
	- **Who**: CLAIM-BENCH dataset with 300+ claim-evidence pairs across multiple research domains
```

**Key elements:**
- Bullet point with discrete empirical result
- Tag: `#evd-candidate`
- Block reference at END of line: `^evd-xxx` (unique ID per paper)
- Subbullets (indented with tab) organized into three categories:
  - **What**: Observable measures/data collected (e.g., metrics, outcomes, variables measured)
  - **How**: Procedures/analyses/experimental design (e.g., methods, statistical tests, interventions)
  - **Who**: Participants/dataset/population (e.g., sample characteristics, dataset details, generalization target)

### Paper Markdown Template
Each paper file in `evidence/` (prefixed with `@`) includes:

```markdown
# [Paper Title]

**Authors:** [Authors]
**Year:** [Year]
**DOI:** [DOI]
**Citation Count:** [Count]

## Evidence Items

- [Evidence 1 text] #evd-candidate ^evd-001
	- **What**: [Observable measures/data collected]
	- **How**: [Procedures/analyses/experimental design]
	- **Who**: [Participants/dataset/population]
- [Evidence 2 text] #evd-candidate ^evd-002
	- **What**: [Observable measures/data collected]
	- **How**: [Procedures/analyses/experimental design]
	- **Who**: [Participants/dataset/population]
- [Evidence 3 text] #evd-candidate ^evd-003
	- **What**: [Observable measures/data collected]
	- **How**: [Procedures/analyses/experimental design]
	- **Who**: [Participants/dataset/population]
```

**Note:** File name format is `@[first-author-lastname]-[year].md` (e.g., `@javaji-2025.md`)

## Extraction Strategy

### 1. Evidence Extraction (Per Paper)
For each paper in the CSV, extract discrete empirical results from:
- **Performance Results** field: Specific metrics, comparative results, statistical findings
- **Key Findings** field: Important patterns, strengths/weaknesses identified
- **Evaluation Setup** field: Context about datasets, metrics, experimental design
- **Supporting quotes/tables**: Additional empirical details

**AI Prompt Strategy:**
- Identify discrete, empirical results (quantitative or qualitative)
- Focus on findings that can support/oppose broader claims
- Include specific metrics, comparisons, and statistical evidence
- Extract 3-10 evidence items per paper depending on richness
- **For each evidence item, generate subbullet notes organized by What/How/Who:**
  - **What**: Observable measures/data collected (e.g., accuracy metrics, performance scores, effect sizes)
  - **How**: Procedures/analyses/experimental design (e.g., prompting approaches, statistical tests, evaluation methods, interventions)
  - **Who**: Participants/dataset/population (e.g., dataset name and size, model types tested, sample characteristics, generalization target)

### 2. Claims Synthesis (Across Papers)
Analyze all extracted evidence to generate high-level claims:
- Identify patterns across multiple papers
- Synthesize comparative findings (e.g., model type performance)
- Identify methodological patterns (e.g., prompting strategies)
- Note contradictions or nuances

**Example Claim Categories:**
- Model performance comparisons (open vs. closed source)
- Prompting strategy effectiveness
- Domain/task-specific findings
- Methodological best practices
- Performance factors and moderators

### 3. Claim-Evidence Linking
- Each claim links to 1+ evidence items that support/oppose it
- Use markdown block reference syntax: `[[evidence/@paper-file.md#evd-id]]`
- Note the `@` prefix in paper file names
- Multiple evidence items can support the same claim
- Evidence items may inform multiple claims

## Implementation Steps

1. **Parse CSV**: Read all papers and structured fields
2. **Extract Evidence**: For each paper, use LLM to identify discrete empirical results
3. **Generate Paper Files**: Create markdown file per paper with evidence items
4. **Synthesize Claims**: Use LLM to analyze all evidence and generate candidate claims
5. **Link Claims to Evidence**: Map each claim to supporting evidence block references
6. **Generate Claims File**: Create central-claims.md with linked claims

## Technical Implementation

### Tools/Libraries
- Python with pandas (CSV parsing)
- Anthropic Claude API (for evidence extraction and claim synthesis)
- File naming: Sanitized author-year format with `@` prefix (e.g., `@javaji-2025.md`)

### Evidence ID Generation
- Format: `^evd-001`, `^evd-002`, etc.
- Sequential numbering per paper
- Three-digit padding for sorting

### Paper File Naming Convention
- Pattern: `@[first-author-lastname]-[year].md`
- Prefixed with `@` symbol
- Lowercase, hyphenated
- Example: `@javaji-2025.md`

## Research Question

**Target Question:** How effective are AI systems (ranging from older task-specific models to LLMs and LLM-powered models) at the task of estimating entailment between claims (e.g., for applications like claim verification and fact checking)?

This question will guide:
- Which evidence items to extract (focus on effectiveness metrics, comparisons across system types)
- What claims to synthesize (performance patterns, factors affecting effectiveness)
- How to organize findings (by model type, task variation, etc.)

## Configuration Decisions

1. ~~**Target Research Question**~~: ✓ Defined above
2. **LLM API Choice**: ✓ Anthropic Claude API
3. **Field Priority**: ✓ Extract from all substantive fields:
   - AI Systems Tested
   - Entailment Task Definition
   - Evaluation Setup
   - Performance Results
   - Key Findings
   - Contextual Factors
   - Supporting quotes/tables for each field
4. **Claim Scope**: Generate claims at multiple levels (specific findings → broader patterns)

## Next Steps

1. ~~Finalize research question and API choice~~ ✓ Complete
2. Create directory structure (claims/, evidence/, scripts/)
3. Develop extraction script with Claude API integration
4. Run extraction on CSV
5. Review and refine candidate claims and evidence

## Implementation Workflow

The extraction script will:
1. **Load CSV** and parse all papers
2. **For each paper**:
   - Extract evidence from all substantive fields
   - For each evidence item, generate subbullet notes organized by What/How/Who:
     - **What**: Observable measures/data collected
     - **How**: Procedures/analyses/experimental design
     - **Who**: Participants/dataset/population
   - Generate unique evidence IDs (^evd-001, ^evd-002, etc.)
   - Create markdown file with `@` prefix in `evidence/` directory (e.g., `@javaji-2025.md`)
3. **After all papers processed**:
   - Collect all extracted evidence with their What/How/Who notes
   - Use Claude to synthesize candidate claims
   - Map claims to supporting evidence block references
   - Generate `claims/central-claims.md` with linked claims (using `@` prefix in links)

---

# Node Verification with Zotero PDFs

## Overview

On-demand verification system that enriches extracted discourse nodes (Evidence, Claims, etc.) with relevant snippets from source PDFs in Zotero. Uses LLM semantic search to find supporting passages and adds verification sections to evidence markdown files.

## Requirements

- **Zotero Access**: Local SQLite database with BetterBibTeX citation keys
- **Citekey Mapping**: Citation keys stored in Extra field as "Citation Key: XXX"
- **Timing**: On-demand CLI tool, not automatic during extraction
- **Content**: Text quotes with page numbers, figures/tables (Phase 2)
- **Matching**: LLM-based semantic search for relevant passages
- **Presentation**: Verification sections added to evidence markdown files

## Architecture

### Pipeline Components

```
CLI Entry Point (verify_with_zotero.py)
  ↓
Zotero DB Module → Query SQLite, map citekey → PDF path
  ↓
PDF Extractor → Extract text chunks, figures, tables
  ↓
Semantic Search → LLM-based relevance scoring
  ↓
Markdown Updater → Insert verification sections
  ↓
Cache Manager → Cache extractions and LLM scores
```

### File Structure

```
scripts/
├── verify_with_zotero.py           # CLI entry point
└── zotero_verification/            # Package (6 modules)
    ├── zotero_db.py                # SQLite queries
    ├── pdf_extractor.py            # PyMuPDF text extraction
    ├── semantic_search.py          # LLM chunk ranking
    ├── markdown_updater.py         # Markdown manipulation
    ├── cache_manager.py            # Caching layer
    └── config.py                   # Configuration

.cache/
├── pdf_extractions/                # Cached PDF data
└── llm_scores/                     # Cached LLM scores

attachments/verification/           # Extracted images (Phase 2)
└── @citekey/
    ├── fig-1-p5.png
    └── table-2-p12.png
```

## Usage

```bash
# Verify single node
python scripts/verify_with_zotero.py @citekey --node evidence-000

# Verify all Evidence nodes
python scripts/verify_with_zotero.py @citekey --type Evidence

# Verify entire paper
python scripts/verify_with_zotero.py @citekey

# Batch verify multiple papers
python scripts/verify_with_zotero.py @paper1 @paper2 @paper3

# Configuration options
python scripts/verify_with_zotero.py @citekey \
  --top-k 10 \
  --dry-run \
  --verbose
```

## Implementation Details

### Zotero Integration
- Searches BetterBibTeX citation keys in Extra field
- Handles both "Citation Key: XXX" and standard citationKey field
- Fuzzy matching with Levenshtein distance for typos
- Maps citekey → itemID → PDF attachment path
- Supports all Zotero libraries (personal and group)

### PDF Extraction
- **Library**: PyMuPDF (fitz) for speed and accuracy
- **Chunking**: Paragraph-based, 500 word max, 50 word overlap
- **Output**: TextChunk objects with content, page_num, chunk_id
- **Figures/Tables**: Caption detection (Phase 2)

### Semantic Search
- **Approach**: Direct LLM scoring (Claude Sonnet 4.5)
- **Strategy**:
  1. Optional keyword pre-filter (50% reduction)
  2. Batch chunks (20-30 per prompt)
  3. Score each chunk 0-10 for relevance
  4. Return top-k with reasoning
- **Optimization**: Cache scores by (node_content, chunk_id) hash

### Markdown Integration
- Non-destructive updates to evidence files
- Inserts verification section after node's What/How/Who metadata
- Replaces existing verification sections on re-run
- Preserves all other markdown structure

**Format**:
```markdown
### Verification Snippets (evidence-000)

**Text Quotes:**

> "Quoted text from PDF..."
>
> *— Page 5*

**Search Metadata:**
- Verified: 2025-12-10
- Chunks searched: 19
- Snippets found: 5 text
```

### Caching
- **PDF Extractions**: JSON files with text chunks, metadata, file hash
- **LLM Scores**: JSON files with relevance scores and reasoning
- **Invalidation**: PDF hash for extractions, 30 days for LLM scores
- **Performance**: ~80% speedup on cached papers

## Configuration

**Environment Variables** (`.env`):
```bash
ANTHROPIC_API_KEY=sk-ant-...
ZOTERO_DB_PATH=/Users/username/Zotero/zotero.sqlite
ZOTERO_STORAGE_PATH=/Users/username/Zotero/storage
```

**Dependencies** (`requirements.txt`):
```
pymupdf>=1.23.0           # PDF extraction
Pillow>=10.0.0            # Image manipulation
tqdm>=4.65.0              # Progress bars
python-Levenshtein>=0.20.0  # Fuzzy matching
```

## Implementation Status

### Phase 1: Text-Only Verification ✅ Complete
- ✅ Zotero SQLite database integration
- ✅ BetterBibTeX citation key parsing
- ✅ PDF text extraction with chunking
- ✅ LLM semantic search
- ✅ Markdown integration
- ✅ File-based caching
- ✅ CLI with batch processing
- ✅ Error handling and fuzzy matching

**Testing Results**:
- Successfully verified `evidence/@kazemitabaarImprovingSteeringVerification2024.md`
- Extracted 19 text chunks from PDF
- Found 5 relevant snippets (scores 7.0-9.5)
- Added verification section with quotes from pages 2, 3, 11, 12, 15

### Phase 2: Figure/Table Extraction (Future)
- Caption detection ("Figure N:", "Table N:")
- Image region extraction
- PNG rendering at 300 DPI
- Embedding in verification sections

### Phase 3: Obsidian UI Integration (Future)
- Command palette integration
- In-app verification triggers
- Real-time status indicators
- User-defined heuristics from annotations

## Key Design Decisions

- **LLM over embeddings**: Provides reasoning, simpler to implement (can add embeddings later)
- **Paragraph chunking**: Preserves semantic units vs. rigid page-based
- **File-based cache**: Simple, readable, no additional services
- **PNG images**: Obsidian native, universal support
- **Node-specific**: Precise verification vs. paper-level bulk
- **Idempotent**: Re-running replaces, doesn't duplicate

## Error Handling

- **DB not found**: Clear message with path suggestions
- **Citekey not found**: Fuzzy match suggestions with Levenshtein distance
- **PDF missing**: Skip paper, continue with others
- **No snippets found**: Add informative note to verification section
- **LLM API error**: 3 retries with exponential backoff
- **Markdown backup**: Automatic before modification

## Success Criteria

- ✅ CLI locates PDFs from BetterBibTeX citekeys
- ✅ Text snippets are semantically relevant to nodes
- ✅ Verification sections integrate cleanly into markdown
- ✅ Cache reduces processing time significantly
- ✅ Graceful handling of errors and missing data
- 🚧 Figures/tables render in Obsidian (Phase 2)
