# Import the 're' module for working with regular expressions (pattern matching in text)
import re
# Import Page class, expect assertion helper, and TimeoutError from Playwright
from playwright.sync_api import Page, expect, TimeoutError
# Import the Gen_AI module which handles communication with the Gemini AI API
from Resources.Utilities import Gen_AI
# Import the os module for file path and operating system related operations
import os

# Define a class called CommonFunctions that holds reusable browser automation methods
class CommonFunctions:
    # Constructor method that runs when a new CommonFunctions object is created
    def __init__(self, page, test_name):
        # Store the browser page object so all methods can use it
        self.page = page
        # Store the test name for naming screenshots and result files
        self.test_name = test_name
        # Initialize a counter to number screenshots sequentially (0, 1, 2, ...)
        self.index = 0

    # Method to capture a screenshot of the current browser page
    def capture_Screenshot(self):
        # Try to take a screenshot, and handle any errors gracefully
        try:
            # Build the file path for the screenshot using the test name and current index number
            path = f"AutomationResults/{self.test_name}/screenshot_{self.index}.png"
            # Take a screenshot of the page and save it to the specified path
            self.page.screenshot(path=path)
            # Increment the screenshot counter so the next screenshot gets a different name
            self.index += 1
            # Print a confirmation message to the console
            print("Screenshot Captured")
            # Return the file path of the saved screenshot
            return path
        # If anything goes wrong during screenshot capture, handle the error
        except Exception as e:
            # Print an error message showing what went wrong
            print(f"Failed to capture screenshot: {e}")
            # Return None to indicate that no screenshot was saved
            return None

    # Method that uses AI to find a new locator when the original one fails
    def recover_with_ai(self, failed_selector, action_description):
        # Print a message indicating that AI recovery is starting for the failed locator
        print(f"Initiating AI Recovery for locator: {failed_selector}")
        
        # Capture state for AI
        # Take a screenshot of the current page state to send to the AI
        screenshot_path = self.capture_Screenshot()
        # Get the full HTML source code of the current page
        page_source = self.page.content()
        
        # Build a detailed prompt message to send to the AI, describing the problem
        prompt = (
            f"I am running a Playwright test. The following locator failed to find the element: '{failed_selector}'. "
            f"Context: {action_description}. "
            "Please analyze the provided screenshot and page source to identify the correct, unique Playwright locator for this element. "
            "Return ONLY the locator string (e.g., 'text=Submit', '#submit-btn', '//button[@id=\\'submit\\']'). "
            "Do not include any explanation or markdown formatting."
        )
        
        # Try to get a response from the AI and use the suggested locator
        try:
            # Send the prompt, screenshot, and page source to the AI and get a new locator back
            new_locator = Gen_AI.get_response(prompt, screenshot_path, page_source)
            # Clean up response
            # Remove any extra whitespace and backtick characters from the AI's response
            new_locator = new_locator.strip().replace('`', '')
            # Print the locator that the AI suggested
            print(f"AI Suggested Locator: {new_locator}")
            
            # Validate if the response looks like a locator
            # Check if the AI response is too long, contains error messages, or looks like JSON (not a locator)
            if len(new_locator) > 200 or "Error" in new_locator or "{" in new_locator or "Failed" in new_locator:
                # Print a warning that the AI returned something that doesn't look like a valid locator
                print(f"AI returned an invalid locator or error: {new_locator}")
                # Return None to indicate recovery failed
                return None

            # Log the change
            # Open the locator_updates.txt file in append mode to record the locator change
            with open("locator_updates.txt", "a") as f:
                # Write a log entry showing the test name, old locator, and the AI-suggested new locator
                f.write(f"Test: {self.test_name} | Old: {failed_selector} | New: {new_locator}\n")
                
            # Return the new locator suggested by the AI
            return new_locator
        # If anything goes wrong during the AI recovery process, handle the error
        except Exception as e:
            # Print an error message showing what went wrong with AI recovery
            print(f"AI Recovery failed: {e}")
            # Return None to indicate that AI recovery did not succeed
            return None

    # Method to navigate the browser to a given URL
    def create_playwright_session(self, url: str):
        # Navigate the browser page to the specified URL
        self.page.goto(url=url)
        # Capture a screenshot of the page after it loads
        self.capture_Screenshot()
        # Print a confirmation message showing which URL was opened
        print(f"Playwright Session Created with {url}")


    # Method to verify that the page title matches the expected text
    def test_has_title(self, title: str):
        # Capture a screenshot before checking the title
        self.capture_Screenshot()
        # Assert that the page title contains the expected text (using regex matching)
        expect(self.page).to_have_title(re.compile(title))
        # Capture a screenshot after the title check passes
        self.capture_Screenshot()
        # Print a confirmation message showing which title was verified
        print(f"Title Verified with {title}")


    # Method to type text into an input field identified by its placeholder text
    def enter_text_in_textfield(self, selector: str, ext: str):
        # Capture a screenshot before attempting to type
        self.capture_Screenshot()
        # Try to find the input field by placeholder and type into it
        try:
            # Find the element by its placeholder text and fill it with the given text
            self.page.locator(selector).fill(ext)
            # Print a confirmation that the text was entered successfully
            print(f"Text {ext} Entered in {selector}")
        # If the placeholder-based selector fails, try AI recovery
        except Exception as e:
            # Print a message that the original selector failed and AI will be used
            print(f"Failed to enter text in placeholder '{selector}'. Retrying with AI...")
            # Ask the AI to suggest a new locator for this input field
            new_locator = self.recover_with_ai(selector, f"Input field with placeholder '{selector}'")
            # Check if the AI returned a valid new locator
            if new_locator:
                # Use the AI-suggested locator to find the element and type the text
                self.page.locator(new_locator).fill(ext)
                # Print a confirmation that text was entered using the AI-recovered locator
                print(f"Text {ext} Entered in {new_locator} (AI Recovered)")
            # If the AI didn't return a valid locator
            else:
                # Re-raise the original error since recovery failed
                raise e
    
    # Method to type text into an input field identified by an XPath or CSS selector
    def enter_text_in_textfield_using_xpath(self, selector: str, ext: str):
        # Capture a screenshot before attempting to type
        self.capture_Screenshot()
        # Try to find the element by the given selector and type into it
        try:
            # Find the element using the locator string and fill it with the given text
            self.page.locator(selector).fill(ext)
            # Print a confirmation that the text was entered successfully
            print(f"Text {ext} Entered in {selector}")
        # If the selector fails, try AI recovery
        except Exception as e:
            # Print a message that the selector failed and AI will be used
            print(f"Failed to enter text in locator '{selector}'. Retrying with AI...")
            # Ask the AI to suggest a new locator for this input field
            new_locator = self.recover_with_ai(selector, f"Input field with locator '{selector}'")
            # Check if the AI returned a valid new locator
            if new_locator:
                # Use the AI-suggested locator to find the element and type the text
                self.page.locator(new_locator).fill(ext)
                # Print a confirmation that text was entered using the AI-recovered locator
                print(f"Text {ext} Entered in {new_locator} (AI Recovered)")
            # If the AI didn't return a valid locator
            else:
                # Re-raise the original error since recovery failed
                raise e



    # Method to click on an element identified by a selector
    def click_element(self, selector: str):
        # Capture a screenshot before attempting to click
        self.capture_Screenshot()
        # Try to find the element and click it
        try:
            # Find the element using the locator string and click on it
            self.page.locator(selector).click()
            # Print a confirmation that the element was clicked successfully
            print(f"Element Clicked with {selector}")
        # If the selector fails, try AI recovery
        except Exception as e:
            # Print a message that clicking with the original selector failed
            print(f"Failed to click element '{selector}'. Retrying with AI...")
            # Ask the AI to suggest a new locator for this clickable element
            new_locator = self.recover_with_ai(selector, "Clickable element")
            # Check if the AI returned a valid new locator
            if new_locator:
                # Use the AI-suggested locator to find and click the element
                self.page.locator(new_locator).click()
                # Print a confirmation that the element was clicked using the AI-recovered locator
                print(f"Element Clicked with {new_locator} (AI Recovered)")
            # If the AI didn't return a valid locator
            else:
                # Re-raise the original error since recovery failed
                raise e




    # (Commented out) Example test method that navigates to Playwright website and clicks "Get started"
    # def test_get_started_link(self,page: Page):
    #     page.goto("https://playwright.dev/")

    #     # Click the get started link.
    #     page.get_by_role("link", name="Get started").click()

    #     # Expects page to have a heading with the name of Installation.
    #     expect(page.get_by_role("heading", name="Installation")).to_be_visible()