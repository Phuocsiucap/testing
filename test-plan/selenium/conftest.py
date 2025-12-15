"""
PHDshop Selenium Test Configuration
===================================
Pytest configuration and fixtures for Selenium tests
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
class Config:
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:8888')
    API_URL = os.getenv('API_URL', 'http://localhost:8000')
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    
    # Test credentials - Cập nhật theo hệ thống thực tế
    TEST_EMAIL = os.getenv('TEST_EMAIL', 'test@gmail.com')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', '12345678')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '1234')


def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:8888",
        help="Base URL for the application"
    )


@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line or config"""
    return request.config.getoption("--browser") or Config.BROWSER


@pytest.fixture(scope="session")
def headless(request):
    """Get headless option from command line or config"""
    return request.config.getoption("--headless") or Config.HEADLESS


@pytest.fixture(scope="session")
def base_url(request):
    """Get base URL from command line or config"""
    return request.config.getoption("--base-url") or Config.BASE_URL


@pytest.fixture(scope="function")
def driver(browser_name, headless):
    """Create WebDriver instance"""
    
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        
    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver, base_url):
    """Driver with logged in user"""
    from pages.login_page import LoginPage
    
    driver.get(f"{base_url}/#/login")
    login_page = LoginPage(driver)
    login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    
    yield driver


@pytest.fixture(scope="function")
def admin_driver(driver, base_url):
    """Driver with logged in admin"""
    from pages.admin_login_page import AdminLoginPage
    
    driver.get(f"{base_url}/#/admin/login")
    admin_login_page = AdminLoginPage(driver)
    admin_login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
    
    yield driver


# Pytest hooks for reporting
def pytest_html_report_title(report):
    report.title = "PHDshop Selenium Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = f"{screenshot_dir}/{item.name}.png"
            driver.save_screenshot(screenshot_path)
