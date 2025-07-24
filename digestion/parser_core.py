
# 🧠 parser_core.py
# Parses raw input from intake logs into structured glyph sequences.

import re
from datetime import datetime

def extract_entry(raw_line):
    """
    Parses a single line of intake text into a structured dict.
    Expected format:
    [timestamp] PROXY (Project): GLYPHS “quote” (Tags: tag1, tag2)
    """
    pattern = r'\[(.*?)\]\s+(\w+)\s+\((.*?)\):\s+(.*?)\s+“(.*?)”\s+\(Tags:\s+(.*?)\)'
    match = re.match(pattern, raw_line)
    
    if not match:
        return None

    timestamp, proxy, project, glyphs, quote, tags = match.groups()
    return {
        "timestamp": datetime.fromisoformat(timestamp.replace("Z", "+00:00")),
        "proxy": proxy.lower(),
        "project": project.lower(),
        "glyphs": [g for g in glyphs if g.strip()],
        "quote": quote.strip(),
        "tags": [t.strip() for t in tags.split(',')],
        "raw": raw_line
    }
