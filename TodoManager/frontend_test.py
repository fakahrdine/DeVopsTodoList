from playwright.sync_api import sync_playwright
import time
import os

print("====================================")
print("Starting Automated Browser Test...")
print("====================================")

# This pattern ensures the playwright components clean up after themselves
with sync_playwright() as p:
    # Detect if we are running in CI
    is_ci = os.environ.get('CI') == 'true'
    
    # We use headless=False so you can actually watch the browser open if running locally!
    # slow_mo=500 slows down the robot by 500ms per action so human eyes can keep up.
    # In CI, it will run headlessly seamlessly.
    browser = p.chromium.launch(headless=is_ci, slow_mo=0 if is_ci else 500)
    page = browser.new_page()

    print("Navigating to http://127.0.0.1:5000 ...")
    try:
        page.goto("http://127.0.0.1:5000")
    except Exception as e:
        print("ERROR: Could not connect! Make sure your Flask app (app.py) is running in the background.")
        browser.close()
        exit(1)

    print("Typing new task into the form...")
    # Playwright finds the HTML input box by its 'name' attribute
    page.fill("input[name='title']", "Automated Playwright Task")

    print("Clicking the 'Add' button...")
    page.click("button[type='submit']")

    print("Waiting for page to safely reload after submission...")
    time.sleep(1)

    print("Checking if the new task is successfully on the screen...")
    # Get the raw HTML content of the page
    content = page.content()
    
    # Assert visually that our dynamic string works
    if "Automated Playwright Task" in content:
        print("\nSUCCESS! The robot successfully added the task!")
    else:
        print("\nFAILED. The task was not found on the page.")

    # We wait 3 seconds before closing so you can admire the final result
    print("\nTest complete, closing browser in 3 seconds...")
    time.sleep(3)
    browser.close()
