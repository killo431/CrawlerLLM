def export_phone_result(result, phone):
    import json
    path = f"data/output/phone_{phone}.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[Exported] Phone lookup to {path}")
