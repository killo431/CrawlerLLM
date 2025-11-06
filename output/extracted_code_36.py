import pandas as pd

# Inside Job Scraping tab, after jobs = scraper.run()
if jobs:
    df = pd.DataFrame(jobs)
    st.download_button("Download CSV", df.to_csv(index=False), "jobs.csv", "text/csv")
    st.download_button("Download JSON", df.to_json(orient="records", indent=2), "jobs.json", "application/json")

🛡️ Breach Checker Module