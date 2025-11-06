User-Agent: JobScraperBot/1.0 (contact@example.com)


Avoid scraping gated or login-required content

5. 🧪 Error Handling & Logging

Checklist

[ ] Define logging level

[ ] Specify retry logic and alerting

Guidelines

Use loguru for structured logging

Retry transient errors with exponential backoff

Log failed URLs and reasons

Optional: integrate alerts via email or Slack

6. 🧬 Testing & Validation

Checklist

[ ] Define success criteria

[ ] Provide sample pages/test cases

[ ] Plan cross-site testing

Guidelines

Validate:

Field completeness

Accuracy

No duplicates

Use pytest for unit tests

Mock HTML for repeatable test cases

7. 🚀 Deployment & Maintenance

Checklist

[ ] Choose deployment platform

[ ] Assign maintenance responsibilities

[ ] Plan for site updates

Guidelines

Use cron jobs, GitHub Actions, or cloud functions

Monitor for HTML structure changes

Version control site adapters (e.g., indeed_v1.py, indeed_v2.py)

8. 📚 Documentation & Support

Checklist

[ ] Define documentation scope

[ ] Include guide for adding new sites

[ ] Identify target audience

Guidelines

Include:

Setup instructions

Usage guide

Config reference

Troubleshooting tips

Tailor docs for developers and analysts

Use Markdown or Sphinx for clean formatting

Would you like this formatted into a Markdown file or Google Doc for team distribution? I can also generate a spreadsheet to track site-specific compliance, field mappings, and adapter status.

You said

STAGES.PROMPT.txt

Plain Text

Create MD file and then utilize custom prompts based on the stage
Copilot said

Here’s the Markdown file you requested, structured to support your multi-agent scraping project using the custom roles from your STAGES.PROMPT.txt. This file can serve as a foundational project artifact and guide for switching between Research, Planning, and Implementation stages.

🧠 AI Job Scraping Agent – Project Blueprint
🔍 Stage: Research Analyst (slug: research-analyst)

Role Summary:
You are Roo, a Data Intelligence Specialist. Your mission is to gather exhaustive, accurate, and actionable intelligence on job boards, scraping constraints, and technical requirements.

Research Objectives

Identify top job boards and their scraping policies

Extract required data fields per site

Document robots.txt  and TOS compliance

Evaluate anti-bot mechanisms and dynamic content usage

Deliverables

site_compliance_matrix.csv

robots_and_tos_summary.md

dynamic_content_flags.json

proxy_requirements.md

📊 Stage: Project Planner (slug: project-plan)

Role Summary:
You are the Project Setup and Initialization Specialist. Your job is to transform research into a structured implementation plan.

Planning Objectives

Define architecture (modular scraper, adapters, storage)

Select tech stack (Python, Scrapy, Playwright, etc.)

Establish compliance and error-handling protocols

Create a phased roadmap with milestones

Deliverables

implementation_plan.md

architecture_diagram.png

config.yaml (site-specific settings)

team_roles_and_assignments.md

💻 Stage: Code (ACT) (slug: code)

Role Summary:
You are ACT, the Implementation Agent. Your job is to write clean, modular, and testable code based on the approved plan.

Implementation Objectives

Scaffold base scraper and adapters

Integrate Playwright for dynamic content

Implement logging, retries, and deduplication

Write unit tests and validation scripts

Deliverables

job_scraper/ (codebase)

tests/ (unit tests)

main.py (entry point)

README.md (usage and setup)
