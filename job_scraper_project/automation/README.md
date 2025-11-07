# Application Submission Automation

Automated job application submission engine supporting multiple platforms.

## Features

✅ **Multi-Platform Support**
- LinkedIn Easy Apply
- Indeed applications
- Greenhouse ATS
- Generic fallback for unknown platforms

✅ **Intelligent Form Detection**
- Automatic field detection and mapping
- Multi-step form navigation
- Document upload automation
- CAPTCHA detection

✅ **Production Ready**
- Comprehensive error handling
- Retry logic with exponential backoff
- Rate limiting to avoid detection
- Screenshot capture for debugging
- Detailed logging

✅ **Flexible Integration**
- CLI interface
- Python API
- Streamlit dashboard
- Batch submission support

## Quick Start

### CLI Usage

Submit a single application:

```bash
python main.py submit \
  --job-url "https://www.linkedin.com/jobs/apply/123456" \
  --resume "/path/to/resume.pdf" \
  --cover-letter "/path/to/cover_letter.pdf" \
  --first-name "John" \
  --last-name "Doe" \
  --email "john.doe@example.com" \
  --phone "555-0123" \
  --linkedin-url "https://linkedin.com/in/johndoe" \
  --headless
```

Batch submission from CSV:

```bash
python main.py submit-batch \
  --jobs-file jobs.csv \
  --resume "/path/to/resume.pdf" \
  --first-name "John" \
  --last-name "Doe" \
  --email "john.doe@example.com" \
  --phone "555-0123"
```

### Python API Usage

```python
import asyncio
from automation import ApplicationSubmitter, SubmissionConfig, ApplicationData

# Create configuration
config = SubmissionConfig(
    headless=True,
    max_retries=3,
    screenshot_on_error=True
)

# Create job dictionary
job = {
    'id': 'job_123',
    'application_url': 'https://www.linkedin.com/jobs/apply/123456'
}

# Create user profile
user_profile = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john.doe@example.com',
    'phone': '555-0123',
    'linkedin_url': 'https://linkedin.com/in/johndoe'
}

# Submit application
async def submit():
    with ApplicationSubmitter(config) as submitter:
        result = await submitter.submit_application(
            job=job,
            resume='/path/to/resume.pdf',
            cover_letter='/path/to/cover_letter.pdf',
            user_profile=user_profile
        )
        
        if result.success:
            print(f"Success! Confirmation: {result.confirmation_number}")
        else:
            print(f"Failed: {result.error_message}")

asyncio.run(submit())
```

### Dashboard Usage

1. Start the dashboard:
```bash
streamlit run dashboard/app.py
```

2. Navigate to "Application Submission" tab
3. Fill in your information and job details
4. Upload resume and cover letter
5. Click "Submit Application"

## Architecture

### Core Components

**application_submitter.py** - Main orchestrator
- Platform detection
- Browser management
- Handler routing
- Rate limiting
- Batch processing

**models.py** - Data models
- `SubmissionResult` - Submission outcomes
- `ApplicationData` - User profile data
- `FormField` - Form field detection
- `NavigationState` - Multi-step tracking
- `SubmissionConfig` - Configuration

**form_mapper.py** - Form intelligence
- Field detection using heuristics
- Label/placeholder analysis
- Field type inference
- Purpose detection

**document_uploader.py** - File uploads
- Resume upload automation
- Cover letter handling
- Format validation
- Upload verification

**navigation.py** - Multi-step forms
- Step detection
- Next/back navigation
- Progress tracking
- Validation

### Platform Handlers

**base_handler.py** - Abstract base
- Common utilities
- Screenshot capture
- CAPTCHA detection
- Form filling helpers

**linkedin_handler.py** - LinkedIn Easy Apply
- Multi-step form navigation
- Screening questions
- Document uploads
- Confirmation detection

**indeed_handler.py** - Indeed applications
- Indeed-hosted vs external detection
- Resume upload
- Form filling
- Confirmation tracking

**greenhouse_handler.py** - Greenhouse ATS
- Standard form structure
- Required field detection
- Custom questions
- Privacy policy acceptance

**generic_handler.py** - Universal fallback
- Heuristic form detection
- Best-effort submission
- Flexible field mapping

## Configuration

Edit `config.yaml` to customize behavior:

```yaml
automation:
  submission:
    enabled: true
    platforms:
      - linkedin
      - indeed
      - greenhouse
      - generic
    retry_attempts: 3
    retry_delay: 5
    screenshot_on_error: true
    screenshot_on_success: true
    captcha_detection: true
    
  rate_limiting:
    enabled: true
    applications_per_hour: 10
    delay_between_submissions: 30
    
  browser:
    headless: false
    slow_mo: 100
    page_load_timeout: 30
```

## Screenshots

Screenshots are automatically captured:
- On successful submission (if enabled)
- On error (if enabled)
- When CAPTCHA is detected
- At each major step (optional)

Saved to: `data/screenshots/{job_id}_{step}_{timestamp}.png`

## Rate Limiting

Built-in rate limiting prevents detection:
- Maximum applications per hour (configurable)
- Delay between submissions (configurable)
- Delay between form actions (configurable)
- Random timing variations

## Error Handling

Comprehensive error handling includes:
- Retry logic with backoff
- CAPTCHA detection and pause
- Network error recovery
- Form validation errors
- Screenshot capture on failure

## Testing

Run tests:
```bash
pytest tests/test_application_submitter.py
pytest tests/test_form_mapper.py
pytest tests/test_models.py
```

All tests are mocked and don't require browser installation.

## Limitations

- **CAPTCHA**: Requires manual intervention
- **Complex Forms**: May need manual submission
- **External Redirects**: Limited support
- **Custom ATS**: Use generic handler
- **Rate Limits**: Platform-dependent

## Best Practices

1. **Test First**: Test on a few applications before batch
2. **Monitor**: Watch the first few submissions
3. **Rate Limit**: Don't exceed 10/hour to avoid detection
4. **Headless**: Use headless mode for production
5. **Screenshots**: Enable for debugging
6. **Verify**: Always verify submissions manually
7. **Privacy**: Store credentials securely

## Troubleshooting

**Application fails immediately**
- Check URL is correct
- Verify resume file exists
- Ensure all required fields are filled

**CAPTCHA detected**
- Solve manually when paused
- Reduce submission rate
- Use residential proxies (advanced)

**Form not filled correctly**
- Check user profile data
- Review screenshot
- Use non-headless mode to debug

**Rate limited**
- Reduce applications per hour
- Increase delay between submissions
- Wait before retrying

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review screenshots in `data/screenshots/`
3. Enable verbose logging
4. Open an issue on GitHub

## Security

⚠️ **Important Security Notes**:
- Never commit credentials
- Use environment variables for secrets
- Review code before running on live accounts
- Be aware of platform Terms of Service
- Use at your own risk

## License

See LICENSE file in the repository root.
