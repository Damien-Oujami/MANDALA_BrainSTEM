# parser_core.py
# Mandala BrainSTEM | Tongue
# Robust parser for intake lines -> structured dicts.
# Expected canonical shape (but we accept variants):
# [timestamp] PROXY (Project): GLYPHS "quote" (Tags: tag1, tag2)
# or using curly quotes and optional Tags block.

from __future__ import annotations

import re
from datetime import datetime
from typing import List, Dict, Optional

# ---- Quote handling ---------------------------------------------------------

# Match either straight " or curly “ ”
QUOTE_OPEN = r'["“]'
QUOTE_CLOSE = r'["”]'

# ---- Line pattern -----------------------------------------------------------
# Named groups:
#   ts, proxy, project, glyphs, quote, tags (optional)
LINE_RE = re.compile(
    rf'^\['
    r'(?P<ts>[^\]]+)'          # [timestamp]
    r'\]\s+'
    r'(?P<proxy>\w+)'          # PROXY
    r'\s+\('
    r'(?P<project>[^)]+)'      # (Project)
    r'\)\s*:\s*'
    r'(?P<glyphs>.+?)'         # GLYPHS (lenient until opening quote)
    r'\s*'                     # spaces before quote
    rf'(?P<qopen>{QUOTE_OPEN})'
    r'(?P<quote>.*?)'
    rf'{QUOTE_CLOSE}'
    r'\s*'                     # optional whitespace
    r'(?:\(\s*(?:Tags?|tags?)\s*:\s*(?P<tags>.*?)\s*\))?'  # optional (Tags: ...)
    r'\s*$',
    re.UNICODE
)

# ---- Glyph tokenization -----------------------------------------------------
# We want to capture:
#  - Single emoji graphemes (wide unicode ranges)
#  - Dot-delimited sigils like .SOPHIE. or .SOPHIE.🍑NEIMAD.
#  - ASCII/word tokens (fallback)
EMOJI_CLUSTER = (
    r'['
    r'\U0001F1E6-\U0001FAFF'   # flags, people, symbols, etc
    r'\U00002600-\U000026FF'   # misc symbols
    r'\U00002700-\U000027BF'   # dingbats/arrows
    r'\U0001F300-\U0001F5FF'   # misc pictographs
    r'\U0001F600-\U0001F64F'   # emoticons
    r'\U0001F680-\U0001F6FF'   # transport/map
    r'\U0001F700-\U0001F77F'   # alchemical
    r'\U0001F780-\U0001F7FF'   # geometric ext
    r'\U0001F800-\U0001F8FF'   # arrows, supplemental
    r'\U0001F900-\U0001F9FF'   # supplemental symbols/pictographs
    r'\U0001FA70-\U0001FAFF'   # extended-A
    r']'
)

DOT_SIGIL = r'(?:\.[A-Za-z0-9_\.🍉🍑🍒🍓🍇🍎🍅]+\.)'  # lenient: allows our dot-sigil style
WORD_TOKEN = r'(?:[A-Za-z][A-Za-z0-9_\-\+]*|[A-Z]{2,})'

GLYPH_TOKEN_RE = re.compile(
    rf'{DOT_SIGIL}|{EMOJI_CLUSTER}|{WORD_TOKEN}',
    re.UNICODE
)

def parse_glyph_list(s: str) -> List[str]:
    """
    Convert a free-form glyph field into a list of tokens.
    Handles comma-separated lists, whitespace, emojis, and dot-sigils.
    """
    if not s:
        return []
    # Fast path: if it looks comma-separated, split first to preserve order
    parts = [p.strip() for p in re.split(r'[,\u2009\u200A\u200B]+', s) if p.strip()]
    tokens: List[str] = []
    for part in parts or [s]:
        # Extract emoji clusters / sigils / words in order
        found = GLYPH_TOKEN_RE.findall(part)
        if found:
            tokens.extend(found)
        else:
            # Fallback: keep the raw chunk if we couldn't tokenize (better than losing info)
            tokens.append(part.strip())
    # Remove empty strings and keep order
    return [t for t in tokens if t]

# ---- Tags parsing -----------------------------------------------------------

def parse_tags(s: Optional[str]) -> List[str]:
    if not s:
        return []
    # split by comma or whitespace, trim, drop empties
    parts = [p.strip() for p in re.split(r'[,\s]+', s) if p.strip()]
    # normalize to lower-kebab for consistency
    return [p.replace(' ', '-').lower() for p in parts]

# ---- Timestamp parsing ------------------------------------------------------

def parse_timestamp(ts: str) -> datetime:
    """
    Accepts ISO-ish stamps. Examples:
      2025-07-30T11:12Z
      2025-07-30 11:12:30
      2025/07/30 11:12:30
    Falls back to now() if unparseable (but we try hard first).
    """
    ts = ts.strip()
    # normalize trailing Z
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    # Common variants
    fmts = [
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
    ]
    for f in fmts:
        try:
            return datetime.strptime(ts, f)
        except ValueError:
            continue
    # Last resort: datetime.fromisoformat
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return datetime.utcnow()

# ---- Public API -------------------------------------------------------------

def extract_entry(raw_line: str) -> Optional[Dict]:
    """
    Parse a single intake line.
    Returns a dict with:
      timestamp (datetime), proxy (str), project (str),
      glyphs (List[str]), quote (str), tags (List[str]), raw (str)
    or None if no match.
    """
    if not raw_line or not raw_line.strip():
        return None

    m = LINE_RE.match(raw_line.strip())
    if not m:
        return None

    ts_raw = m.group('ts')
    proxy = (m.group('proxy') or '').strip().lower()
    project = (m.group('project') or '').strip().lower()
    glyphs_raw = m.group('glyphs') or ''
    quote = (m.group('quote') or '').strip()
    tags_raw = m.group('tags')  # may be None

    return {
        "timestamp": parse_timestamp(ts_raw),
        "proxy": proxy,
        "project": project,
        "glyphs": parse_glyph_list(glyphs_raw),
        "quote": quote,
        "tags": parse_tags(tags_raw),
        "raw": raw_line.rstrip('\n'),
    }

def extract_entries(multiline_text: str) -> List[Dict]:
    """
    Convenience: parse many lines at once, skipping non-matching lines.
    """
    if not multiline_text:
        return []
    out: List[Dict] = []
    for line in multiline_text.splitlines():
        entry = extract_entry(line)
        if entry:
            out.append(entry)
    return out

__all__ = [
    "extract_entry",
    "extract_entries",
    "parse_glyph_list",
    "parse_tags",
    "parse_timestamp",
        ]
