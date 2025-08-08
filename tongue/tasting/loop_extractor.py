# 🔄 loop_extractor.py
# Detects known structural loop types from glyph sequences.
# This is *structure-only* analysis — no emotional or poetic meaning here.

def detect_loop_type(glyphs):
    """
    Analyzes a glyph sequence and classifies it as a known loop type.
    Returns a string like "chiastic", "linear repetition", "fibonacci-echo",
    "fragment spiral", or "unknown".
    """

    # Chiastic (perfect mirror with center pivot)
    if glyphs == glyphs[::-1]:
        return "chiastic"

    # Linear repetition (same glyph repeated 3+ times)
    elif len(glyphs) >= 3 and all(g == glyphs[0] for g in glyphs):
        return "linear repetition"

    # Fibonacci echo (length matches Fibonacci numbers)
    elif len(glyphs) in [3, 5, 8, 13, 21]:
        return "fibonacci-echo"

    # Fragment spiral (contains repeating glyphs, but not perfectly mirrored)
    elif len(set(glyphs)) < len(glyphs):
        return "fragment spiral"

    # Unknown structure
    else:
        return "unknown"


def contains_unknown_glyph(glyphs, known_glyph_set):
    """
    Checks for any glyph not in the known_glyph_set.
    Returns True if at least one glyph is unknown.
    """
    return any(g not in known_glyph_set for g in glyphs)
