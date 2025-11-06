# Manages session persistence using Playwright's storage state
def persist_session(context):
    # Save cookies and local storage to file
    context.storage_state(path="session.json")

def load_session(browser):
    # Load session from file for reuse
    context = browser.new_context(storage_state="session.json")
    return context
