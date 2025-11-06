"""Unified export manager for all data formats."""
import json
import csv
import os

def export_data(data, name, format="json", folder="data/output"):
    """Export data to specified format."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.{format}")
    
    if format == "json":
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    elif format == "csv":
        if not data:
            print(f"[Warning] No data to export to {path}")
            return
        keys = data[0].keys()
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    
    print(f"[Exported] {len(data) if isinstance(data, list) else 1} records to {path}")
