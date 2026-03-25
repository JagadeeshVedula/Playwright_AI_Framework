# Import the CommonFunctions class and give it a short alias 'check' for convenience
from Resources.Common.CommonFunctions import CommonFunctions as check

# Define a class called LoginPage that contains the login workflow steps
class LoginPage:
    # Method that performs the login steps on Amazon's website
    def login(self,page,test_name,username):
        # Create an instance of CommonFunctions with the browser page and test name
        common = check(page,test_name)
        # Navigate the browser to Amazon India's homepage
        common.create_playwright_session("https://www.amazon.in/")
        # Verify that the page title contains "Online Shopping"
        common.test_has_title("Online Shopping")
        # Click on the "Hello, sign in" text to open the sign-in menu
        common.click_element("xpath=//span[text()='Hello, sign in']")
        # (Commented out) Alternative selector for clicking a "Sign in" button
        # common.click_element("xpath=//span[text()='Sign in']")
        # Click on the email input field to focus it
        common.click_element("xpath=//input[@name='email']")
        # Type the username (email/phone) into the email input field
        common.enter_text_in_textfield_using_xpath("xpath=//input[@name='email']",username)
        # Click the "Continue" button to proceed to the next step
        common.click_element("xpath=//span[@id='continue']")