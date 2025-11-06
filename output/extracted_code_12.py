# Configuration file for site-specific settings and global scraping parameters

global:
  headless: true
  crawl_delay: 2  # seconds between requests
  max_retries: 3
  output_format: json
  use_llm_brain: true
  proxy_rotation: true

proxies:
  provider: "Smartproxy"
  username: "your_proxy_user"
  password: "your_proxy_pass"
  endpoint: "http://proxy.smartproxy.com:8000"

sites:
  indeed:
    dynamic: true
    pagination_selector: "a[aria-label='Next']"
    job_card_selector: ".job_seen_beacon"
    fields:
      title: "h2"
      company: ".companyName"
      location: ".companyLocation"
      description: ".job-snippet"
      link: "a"
    robots_txt: false
    tos_restricted: true
    requires_proxy: true
