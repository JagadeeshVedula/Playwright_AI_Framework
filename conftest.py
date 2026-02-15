import pytest
from playwright.sync_api import sync_playwright
import os


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser,request):
    test_name=request.node.name
    context=browser.new_context(no_viewport=False,record_video_dir=f"AutomationResults/{test_name}/")
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page=context.new_page()
    # page = browser.new_page()
    yield page
    page.close()
    context.tracing.stop(path=f"AutomationResults/{test_name}/trace.zip")
    context.close()

@pytest.fixture
def test_name(request):
    test_name=request.node.name
    yield test_name

