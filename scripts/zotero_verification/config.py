"""Configuration constants for Zotero PDF verification system."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
ATTACHMENTS_DIR = PROJECT_ROOT / "attachments" / "verification"
CACHE_DIR = PROJECT_ROOT / ".cache"
PDF_CACHE_DIR = CACHE_DIR / "pdf_extractions"
LLM_CACHE_DIR = CACHE_DIR / "llm_scores"

# Zotero configuration
ZOTERO_DB_PATH = Path(os.getenv("ZOTERO_DB_PATH", "~/.zotero/zotero.sqlite")).expanduser()
ZOTERO_STORAGE_PATH = Path(os.getenv("ZOTERO_STORAGE_PATH", "~/Zotero/storage")).expanduser()

# PDF extraction settings
MAX_CHUNK_WORDS = 500
CHUNK_OVERLAP_WORDS = 50
IMAGE_DPI = 300

# LLM settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Search settings
DEFAULT_TOP_K = 5
KEYWORD_PREFILTER_RATIO = 0.5  # Keep top 50% after keyword filter

# Cache settings
CACHE_EXPIRY_DAYS = 30
