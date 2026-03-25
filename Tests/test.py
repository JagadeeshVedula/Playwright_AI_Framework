# Import the time module (available for adding delays if needed)
import time
# Import CommonFunctions class and give it a short alias 'check' for convenience
from Resources.Common.CommonFunctions import CommonFunctions as check
# (Commented out) Alternative import for fixtures from a local conftest file
# from Resources.Common.conftest import page,browser,test_name




# Define a test function that verifies the Amazon homepage title and searches for a product
def test_homepage_title(page,test_name):
    """Test capturing screenshot and verifying title"""
    # Create an instance of CommonFunctions with the browser page and test name
    common = check(page,test_name)
    # Navigate the browser to the Amazon India homepage
    common.create_playwright_session("https://www.amazon.in/")
    # Verify that the page title contains "Online Shopping"
    # common.test_has_title("Online Shopping")
    # Call the helper function to search for a product on the page
    search_for_product(page,test_name)
    # Click the search submit button using its XPath selector
    common.click_element('xpath=//input[@type="submit"]')
    # Verify that the page title now contains "shoes for man" (search results page)
    common.test_has_title("shoes for man")

# Define a helper function that types a search query into the Amazon search bar
def search_for_product(page,test_name):
    # Create an instance of CommonFunctions with the browser page and test name
    common = check(page,test_name)
    # Find the search input field by its placeholder text and type the search query into it
    common.enter_text_in_textfield('Search Amazon.in',"shoes for man stylish")
