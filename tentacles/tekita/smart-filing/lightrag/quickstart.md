# LightRAG Quickstart

```python
import os
from lightrag import LightRAG, QueryParam

DATA_DIR = "data/company_graph"
os.makedirs(DATA_DIR, exist_ok=True)

rag = LightRAG(DATA_DIR)
rag.insert(["hello world"])
print(rag.query("hello", param=QueryParam(mode="hybrid")))
```

Modes: `naive`, `local`, `global`, `hybrid`.
