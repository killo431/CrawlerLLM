import json
import csv
import os

def export_data(data, name, format="json", folder="data/output"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.{format}")

    if format == "json":
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    elif format == "csv":
        keys = data[0].keys() if data else []
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    print(f"[Exported] {len(data)} records to {path}")

🔁 Refactor OSINT Modules to Use Export Manager
scrapers/osint/phone_lookup.py
from core.export_manager import export_data

def export_phone_result(result, phone):
    export_data(result, f"phone_{phone}", format="json")

scrapers/osint/footprint_trace.py
from core.export_manager import export_data

def export_footprint_result(result, name):
    export_data(result, f"footprint_{name.replace(' ', '_')}", format="json")

scrapers/osint/breach_checker.py
from core.export_manager import export_data

def export_breach_result(result, email):
    export_data(result, f"breach_{email.replace('@', '_at_')}", format="json")
