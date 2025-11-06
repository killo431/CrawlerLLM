import requests

def lookup_phone(phone_number: str) -> dict:
    # Use Numverify (free tier) or scrape OSINT Broker
    try:
        response = requests.get(f"https://api.numlookupapi.com/v1/validate?number={phone_number}")
        data = response.json()
        return {
            "valid": data.get("valid"),
            "carrier": data.get("carrier"),
            "location": data.get("location"),
            "line_type": data.get("line_type"),
            "country": data.get("country_name")
        }
    except Exception as e:
        return {"error": str(e)}
