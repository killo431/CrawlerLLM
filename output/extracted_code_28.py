import requests

def generate_feature_plan(feature_description: str) -> str:
    prompt = f"""
You are an AI Feature Developer for an OSINT + Job Scraping Dashboard.
Given this feature request: '{feature_description}', do the following:
1. Break it into subtasks
2. Suggest file/module names
3. Recommend external tools or APIs
4. Identify integration points in the existing architecture
Return as structured JSON.
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]
