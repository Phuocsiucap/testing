"""
Base Page Object
================
Contains common methods and properties for all page objects
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def open(self, url):
        """Navigate to URL"""
        self.driver.get(url)
        return self
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_title(self):
        """Get page title"""
        return self.driver.title
    
    def find_element(self, locator):
        """Find element with explicit wait"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Find multiple elements"""
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        """Click on element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return self
    
    def type_text(self, locator, text, clear=True):
        """Type text into input field"""
        element = self.find_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)
        return self
    
    def get_text(self, locator):
        """Get text from element"""
        return self.find_element(locator).text
    
    def get_attribute(self, locator, attribute):
        """Get attribute value from element"""
        return self.find_element(locator).get_attribute(attribute)
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be visible"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    def wait_for_url_contains(self, text, timeout=None):
        """Wait for URL to contain specific text"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        return self
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        return self
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self
    
    def hover(self, locator):
        """Hover over element"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        return self
    
    def drag_and_drop(self, source_locator, target_locator):
        """Drag and drop element"""
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()
        return self
    
    def switch_to_frame(self, locator):
        """Switch to iframe"""
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
        return self
    
    def switch_to_default_content(self):
        """Switch back to main content"""
        self.driver.switch_to.default_content()
        return self
    
    def accept_alert(self):
        """Accept browser alert"""
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        return self
    
    def dismiss_alert(self):
        """Dismiss browser alert"""
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()
        return self
    
    def get_alert_text(self):
        """Get text from alert"""
        self.wait.until(EC.alert_is_present())
        return self.driver.switch_to.alert.text
    
    def take_screenshot(self, filename):
        """Take screenshot"""
        self.driver.save_screenshot(filename)
        return self
    
    def execute_script(self, script, *args):
        """Execute JavaScript"""
        return self.driver.execute_script(script, *args)
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to fully load"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self
    
    def refresh(self):
        """Refresh page"""
        self.driver.refresh()
        return self
    
    def go_back(self):
        """Go back to previous page"""
        self.driver.back()
        return self
    
    def go_forward(self):
        """Go forward"""
        self.driver.forward()
        return self
