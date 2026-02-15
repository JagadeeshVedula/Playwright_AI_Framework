from Resources.Common.CommonFunctions import CommonFunctions as check
class LoginPage:
    def login(self,page,test_name,username):
        common = check(page,test_name)
        common.create_playwright_session("https://www.amazon.in/")
        common.test_has_title("Online Shopping")
        common.click_element("xpath=//span[text()='Hello, sign in']")
        # common.click_element("xpath=//span[text()='Sign in']")
        common.click_element("xpath=//input[@name='email']")
        common.enter_text_in_textfield_using_xpath("xpath=//input[@name='email']",username)
        common.click_element("xpath=//span[@id='continue']")