from Resources.Pages.LoginPage import LoginPage
# from Resources.CommonCommonFunctions import CommonFunctions as check
import time
import csv
import pytest

def load_test_data():
    with open("Data/login_data.csv", newline="") as csvfile:
        return list(csv.reader(csvfile, delimiter=','))

@pytest.mark.parametrize("username,password", load_test_data())
def test_login(page,test_name,username,password):
    """Test capturing screenshot and verifying title"""
    common = LoginPage()
    common.login(page,test_name,username)
   
