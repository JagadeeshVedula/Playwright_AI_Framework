import time
from Resources.Common.CommonFunctions import CommonFunctions as check
# from Resources.Common.conftest import page,browser,test_name




def test_homepage_title(page,test_name):
    """Test capturing screenshot and verifying title"""
    common = check(page,test_name)
    common.create_playwright_session("https://www.amazon.in/")
    common.test_has_title("Online Shopping")
    search_for_product(page,test_name)
    common.click_element('xpath=//input[@type="submit"]')
    common.test_has_title("shoes for man")

def search_for_product(page,test_name):
    common = check(page,test_name)
    common.enter_text_in_textfield('Search Amazon.in',"shoes for man stylish")



