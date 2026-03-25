# Import the LoginPage class that contains the login workflow steps
from Resources.Pages.LoginPage import LoginPage
# (Commented out) Alternative import for CommonFunctions
# from Resources.CommonCommonFunctions import CommonFunctions as check
# Import the time module (available for adding delays if needed)
import time
# Import the csv module for reading test data from CSV files
import csv
# Import the pytest framework for writing and running tests
import pytest

# Define a function that reads test data (username and password) from a CSV file
def load_test_data():
    # Open the CSV file containing login credentials in read mode
    with open("Data/login_data.csv", newline="") as csvfile:
        # Read all rows from the CSV file and return them as a list of lists
        return list(csv.reader(csvfile, delimiter=','))

# Use pytest parametrize to run the test once for each row of data from the CSV file
@pytest.mark.parametrize("username,password", load_test_data())
# Define a test function that tests the login flow with the given username and password
def test_login(page,test_name,username,password):
    """Test capturing screenshot and verifying title"""
    # Create an instance of the LoginPage class
    common = LoginPage()
    # Call the login method to perform the login steps with the given credentials
    common.login(page,test_name,username)
