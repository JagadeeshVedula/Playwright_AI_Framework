import re
from playwright.sync_api import Page, expect, TimeoutError
from Resources.Utilities import Gen_AI
import os

class CommonFunctions:
    def __init__(self, page, test_name):
        self.page = page
        self.test_name = test_name
        self.index = 0

    def capture_Screenshot(self):
        try:
            path = f"AutomationResults/{self.test_name}/screenshot_{self.index}.png"
            self.page.screenshot(path=path)
            self.index += 1
            print("Screenshot Captured")
            return path
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")
            return None

    def recover_with_ai(self, failed_selector, action_description):
        print(f"Initiating AI Recovery for locator: {failed_selector}")
        
        # Capture state for AI
        screenshot_path = self.capture_Screenshot()
        page_source = self.page.content()
        
        prompt = (
            f"I am running a Playwright test. The following locator failed to find the element: '{failed_selector}'. "
            f"Context: {action_description}. "
            "Please analyze the provided screenshot and page source to identify the correct, unique Playwright locator for this element. "
            "Return ONLY the locator string (e.g., 'text=Submit', '#submit-btn', '//button[@id=\\'submit\\']'). "
            "Do not include any explanation or markdown formatting."
        )
        
        try:
            new_locator = Gen_AI.get_response(prompt, screenshot_path, page_source)
            # Clean up response
            new_locator = new_locator.strip().replace('`', '')
            print(f"AI Suggested Locator: {new_locator}")
            
            # Validate if the response looks like a locator
            if len(new_locator) > 200 or "Error" in new_locator or "{" in new_locator or "Failed" in new_locator:
                print(f"AI returned an invalid locator or error: {new_locator}")
                return None

            # Log the change
            with open("locator_updates.txt", "a") as f:
                f.write(f"Test: {self.test_name} | Old: {failed_selector} | New: {new_locator}\n")
                
            return new_locator
        except Exception as e:
            print(f"AI Recovery failed: {e}")
            return None

    def create_playwright_session(self, url: str):
        self.page.goto(url=url)
        self.capture_Screenshot()
        print(f"Playwright Session Created with {url}")


    def test_has_title(self, title: str):
        self.capture_Screenshot()
        expect(self.page).to_have_title(re.compile(title))
        self.capture_Screenshot()
        print(f"Title Verified with {title}")


    def enter_text_in_textfield(self, selector: str, ext: str):
        self.capture_Screenshot()
        try:
            self.page.get_by_placeholder(selector).fill(ext)
            print(f"Text {ext} Entered in {selector}")
        except Exception as e:
            print(f"Failed to enter text in placeholder '{selector}'. Retrying with AI...")
            new_locator = self.recover_with_ai(selector, f"Input field with placeholder '{selector}'")
            if new_locator:
                self.page.locator(new_locator).fill(ext)
                print(f"Text {ext} Entered in {new_locator} (AI Recovered)")
            else:
                raise e
    
    def enter_text_in_textfield_using_xpath(self, selector: str, ext: str):
        self.capture_Screenshot()
        try:
            self.page.locator(selector).fill(ext)
            print(f"Text {ext} Entered in {selector}")
        except Exception as e:
            print(f"Failed to enter text in locator '{selector}'. Retrying with AI...")
            new_locator = self.recover_with_ai(selector, f"Input field with locator '{selector}'")
            if new_locator:
                self.page.locator(new_locator).fill(ext)
                print(f"Text {ext} Entered in {new_locator} (AI Recovered)")
            else:
                raise e



    def click_element(self, selector: str):
        self.capture_Screenshot()
        try:
            self.page.locator(selector).click()
            print(f"Element Clicked with {selector}")
        except Exception as e:
            print(f"Failed to click element '{selector}'. Retrying with AI...")
            new_locator = self.recover_with_ai(selector, "Clickable element")
            if new_locator:
                self.page.locator(new_locator).click()
                print(f"Element Clicked with {new_locator} (AI Recovered)")
            else:
                raise e




    # def test_get_started_link(self,page: Page):
    #     page.goto("https://playwright.dev/")

    #     # Click the get started link.
    #     page.get_by_role("link", name="Get started").click()

    #     # Expects page to have a heading with the name of Installation.
    #     expect(page.get_by_role("heading", name="Installation")).to_be_visible()