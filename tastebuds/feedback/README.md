# TasteBuds Feedback Emitter

Utility for generating feedback files consumed by Tentacles.

Each invocation produces a JSON document named `feedback_###.json` with the following layout:

```json
{
  "type": "symbolic summary",
  "content": "Short description",
  "metadata": {
    "urgency_level": 2,
    "relevance_score": 0.7,
    "tentacle_match": "alpha"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Usage

```bash
python emitter.py "symbolic summary" "Short description" \
    --urgency_level 2 --relevance_score 0.7 --tentacle_match alpha
```

Feedback types currently recognised:

- `new_loop_structure`
- `symbolic summary`
- `function upgrade`
- `warning`
- `emergent chime`
