"""Pipeline to ingest, classify, route, index, and notify for dropped files."""

def run(apply: bool = False, notify: bool = False) -> None:
    """Placeholder intake pipeline."""
    if apply:
        print("Applying file moves...")
    if notify:
        print("Sending notification...")
