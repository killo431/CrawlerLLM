# Simulates human-like interaction to evade bot detection
def simulate_human_interaction(page):
    # Move mouse to a location
    page.mouse.move(100, 200)

    # Wait to simulate human pause
    page.wait_for_timeout(500)

    # Click on the location
    page.mouse.click(100, 200)

    # Type a search query
    page.keyboard.type("Python developer")
