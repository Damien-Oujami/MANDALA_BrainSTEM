# 🔄 loop_extractor.py
# Attempts to detect known loop structures from glyph sequences.

def detect_loop_type(glyphs):
    """
    Analyzes glyph sequence to guess structural pattern.
    Returns loop type string (or 'unknown')
    """
    if glyphs == glyphs[::-1]:
        return "chiastic"
    elif len(glyphs) >= 3 and glyphs[1:] == glyphs[:-1]:
        return "linear repetition"
    elif len(glyphs) in [3, 5, 8, 13, 21]:  # crude Fibonacci anchor
        return "fibonacci-echo"
    elif len(set(glyphs)) < len(glyphs):
        return "fragment spiral"
    else:
        return "unknown"

def contains_unknown_glyph(glyphs, known_glyph_set):
    """
    Checks for presence of unknown glyphs based on known set
    """
    return any(g not in known_glyph_set for g in glyphs)

