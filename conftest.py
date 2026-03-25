# Import the pytest framework for writing and running tests
import pytest
# Import sync_playwright to control browser automation synchronously
from playwright.sync_api import sync_playwright
# Import os module for interacting with the operating system (file paths, etc.)
import os
# Import shutil module for high-level file operations like deleting folders
import shutil


# Define a pytest fixture named 'browser' that provides a browser instance to tests
@pytest.fixture
def browser():
    # Start a Playwright session and assign it to variable 'p'
    with sync_playwright() as p:
        # Launch a Chromium browser in visible mode (headless=False means you can see it)
        browser = p.chromium.launch(headless=True)
        # Provide the browser instance to the test, and pause here until the test finishes
        yield browser
        # After the test finishes, close the browser to free up resources
        browser.close()

# Define a pytest fixture named 'page' that depends on 'browser' and 'request' fixtures
@pytest.fixture
def page(browser,request):
    # Get the name of the currently running test
    test_name=request.node.name
    # Build the folder path where test results (screenshots, videos, traces) will be saved
    path = f"AutomationResults/{test_name}"
    # Check if a results folder for this test already exists
    if os.path.exists(path):
        # If it exists, delete the old results folder and all its contents
        shutil.rmtree(path)
    # Create a fresh results folder for this test (exist_ok=True prevents errors if it already exists)
    os.makedirs(path, exist_ok=True)
    # Create a new browser context with video recording enabled, saving videos to the results folder
    context=browser.new_context(no_viewport=False,record_video_dir=f"{path}/")
    # Start tracing to capture screenshots, DOM snapshots, and source code for debugging
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    # Open a new browser page (tab) within the context
    page=context.new_page()
    # (Commented out) Alternative way to create a page directly from browser without context
    # page = browser.new_page()
    # Provide the page to the test, and pause here until the test finishes
    yield page
    # After the test finishes, close the page
    page.close()
    # Stop tracing and save the trace file as a zip for later analysis
    context.tracing.stop(path=f"AutomationResults/{test_name}/trace.zip")
    # Close the browser context to release all resources
    context.close()

@pytest.fixture(scope="function",autouse=True)
def session():
    print("function execution started")
    yield
    print("function execution ended")
    
# Define a pytest fixture named 'test_name' that provides the current test's name
@pytest.fixture
def test_name(request):
    # Get the name of the currently running test from the request object
    test_name=request.node.name
    # Provide the test name to the test function
    yield test_name
