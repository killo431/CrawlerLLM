import requests

def trace_name(name: str) -> dict:
    # Use WhatsMyName and Epieos for footprint tracing
    try:
        # WhatsMyName CLI or API wrapper (mocked here)
        username = name.replace(" ", "").lower()
        platforms = ["github", "reddit", "twitter"]
        results = {}
        for platform in platforms:
            url = f"https://{platform}.com/{username}"
            r = requests.get(url)
            results[platform] = "Found" if r.status_code == 200 else "Not Found"

        # Epieos reverse lookup (mocked)
        epieos_result = {
            "google_reviews": f"https://epieos.com/reviews/{username}",
            "email_trace": f"https://epieos.com/email/{username}@example.com"
        }

        return {
            "username": username,
            "platform_presence": results,
            "epieos": epieos_result
        }
    except Exception as e:
        return {"error": str(e)}
