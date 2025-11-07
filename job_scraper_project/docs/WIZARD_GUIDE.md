# JobCopilot Configuration Wizard Guide

## Overview

The JobCopilot Configuration Wizard provides a streamlined, step-by-step interface for setting up your job search automation preferences. This guide explains each step of the wizard and how to use it effectively.

## Design Philosophy

The wizard is based on the AiCopilotCFG UX pattern, which uses a **4-step progressive disclosure** approach:
- **Step 1**: Core job preferences (must-have information)
- **Step 2**: Optional filters (nice-to-have refinements)
- **Step 3**: Resume selection (required document)
- **Step 4**: Writing style preferences (personalization)

This design reduces cognitive load and improves completion rates compared to a single-page form.

## Starting the Wizard

### From the Dashboard
1. Open the JobCopilot dashboard: `streamlit run dashboard/jobcopilot_app.py`
2. Click the "⚙️ Setup Wizard" button at the top

### Direct Access
Run directly: `streamlit run dashboard/copilot_wizard.py`

## Step-by-Step Guide

### Step 1: Job Preferences

**Purpose**: Define what jobs you're looking for

**Fields**:
- **Work Location**
  - Remote Jobs: Check if you want remote positions
    - If selected, choose remote locations (Worldwide, USA Only, Europe, etc.)
  - On-site Jobs / Hybrid: Check if you want physical location jobs
    - If selected, specify cities (New York, San Francisco, Austin, etc.)
  - ⚠️ **Validation**: Must select at least one work location option

- **Job Types** (select at least one)
  - Fulltime
  - Part-Time
  - Contractor / Temp
  - Internship
  - ⚠️ **Validation**: Must select at least one job type

- **Job Titles** (up to 5)
  - Enter comma-separated job titles
  - Examples: "Software Engineer, Data Scientist, Product Manager"
  - ⚠️ **Validation**: Must enter at least one job title
  - Maximum 5 titles allowed

**Tips**:
- Be specific with job titles for better matches
- Select multiple locations to expand opportunities
- Mix job types if you're flexible

---

### Step 2: Optional Filters

**Purpose**: Narrow your search with additional criteria

**Fields**:
- **Experience Level** (optional)
  - Select all levels you're qualified for:
    - Internship
    - Entry Level
    - Mid Level
    - Senior Level
    - Lead/Principal
    - Executive

- **Salary Range** (optional)
  - Minimum Salary: Set your expected minimum (USD/year)
  - Maximum Salary: Set your expected maximum (USD/year)
  - ⚠️ Validation: Min must be ≤ Max

**Tips**:
- Leaving filters empty means "no restriction"
- Set salary range slightly below your target to see more opportunities
- Select experience levels you're comfortable with

---

### Step 3: Resume Upload

**Purpose**: Provide your resume for AI-powered applications

**Options**:

1. **Upload New Resume**
   - Click "Choose a file"
   - Supported formats: PDF, DOC, DOCX
   - File size displayed after upload
   - ✅ Confirmation shown when uploaded

2. **Use Existing Resume**
   - Select from previously uploaded resumes
   - Dropdown shows all stored resumes

**Requirements**:
- ⚠️ **Validation**: Must upload or select a resume to continue

**Tips**:
- Use an ATS-friendly format (PDF recommended)
- Ensure resume is up-to-date
- Keep file size under 2MB for best performance

---

### Step 4: Writing Style

**Purpose**: Personalize AI-generated cover letters and applications

**Fields**:

1. **Writing Style** (required)
   - Professional: Formal, business-appropriate
   - Casual: Friendly, conversational
   - Witty: Clever, engaging with personality
   - Academic: Scholarly, research-focused

2. **Tone Scale** (required)
   - Very Formal → Formal → Balanced → Casual → Very Casual
   - Default: Balanced

3. **Advanced Settings** (optional, in expander)
   - **Perplexity (Complexity)**
     - Simple: Clear and direct language
     - Medium: Balanced complexity (default)
     - Complex: Nuanced and sophisticated
   
   - **Burstiness (Variation)**
     - Uniform: Consistent sentence structure
     - Dynamic: Varied rhythm and flow (default, more human-like)

**Configuration Summary**:
- Review your complete setup before finishing
- Shows job preferences and style settings side-by-side

**Completion**:
- Click "🚀 Complete Setup" to save configuration
- Redirects to main dashboard
- Configuration saved for future use

---

## Navigation

### Between Steps
- **Next Step →**: Proceed to next step (validates current step)
- **← Back**: Return to previous step (no validation, preserves data)
- **← Exit**: Return to main dashboard (saves progress)

### Progress Indicator
- Shows "Step X of 4" throughout the wizard
- Visual feedback on current position

---

## Validation Rules

### Step 1 (Required)
✅ At least one work location (remote OR physical)  
✅ At least one job type  
✅ At least one job title (max 5)

### Step 2 (Optional)
⚠️ Salary min ≤ Salary max (if both provided)

### Step 3 (Required)
✅ Resume uploaded OR existing resume selected

### Step 4 (Required)
✅ Writing style selected  
✅ Tone selected

---

## Best Practices

### For Best Results:
1. **Be Specific**: Use exact job titles companies use
2. **Be Flexible**: Select multiple job types and locations
3. **Be Realistic**: Set salary ranges based on market research
4. **Be Authentic**: Choose writing styles that match your personality

### Common Mistakes to Avoid:
❌ Only selecting one job title (limits opportunities)  
❌ Setting salary range too narrow  
❌ Using outdated resume  
❌ Choosing writing style that doesn't match industry norms

---

## Technical Details

### Data Persistence
- Configuration saved to `st.session_state.config`
- Persists across page navigation
- Cleared on browser refresh (future: database storage)

### Resume Storage
- Uploaded files saved to temporary directory
- Path stored in configuration
- Future: Cloud storage integration

### Integration
- Configuration used by:
  - Job matching engine
  - Application generator
  - Cover letter composer
  - Resume optimizer

---

## Troubleshooting

### "Please select at least one option" error
→ Complete all required fields in the current step

### "Maximum 5 job titles allowed" warning
→ Reduce number of comma-separated titles to 5 or fewer

### "Please upload or select a resume" error
→ Upload a new file or select from existing resumes in Step 3

### Button not working
→ Ensure all validation requirements are met for current step

### Lost progress
→ Configuration stored in session, may be lost on browser refresh
→ Complete wizard in one session for best experience

---

## Future Enhancements

Planned improvements:
- [ ] Save/load configuration presets
- [ ] Multiple resume profiles
- [ ] A/B testing different styles
- [ ] Configuration history
- [ ] Import from LinkedIn profile
- [ ] Smart defaults based on industry

---

## Feedback & Support

Found a bug? Have a suggestion?
- Open an issue on GitHub
- Contact support team
- Check documentation for updates

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Based on**: AiCopilotCFG UX Pattern
