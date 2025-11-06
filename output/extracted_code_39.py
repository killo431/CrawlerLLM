def export_footprint_result(result, name):
    import json
    path = f"data/output/footprint_{name.replace(' ', '_')}.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[Exported] Footprint trace to {path}")
