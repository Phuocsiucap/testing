"""
Admin Login Page Object
=======================
Page object for admin login functionality
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class AdminLoginPage(BasePage):
    """Page object for Admin Login page"""
    
    # Locators - Đã cập nhật theo frontend thực tế
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Đăng Nhập')]")
    LOGIN_BUTTON_CSS = (By.CSS_SELECTOR, "button.bg-blue-500, button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, [class*='error'], .text-red-500")
    LOGIN_FORM_TITLE = (By.XPATH, "//h2[contains(text(),'Đăng Nhập')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/#/admin/login"
    
    def open_admin_login_page(self, base_url):
        """Navigate to admin login page"""
        self.open(f"{base_url}{self.url}")
        self.wait_for_page_load()
        return self
    
    def enter_email(self, email):
        """Enter admin email"""
        self.type_text(self.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password):
        """Enter admin password"""
        self.type_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """Click login button"""
        try:
            self.click(self.LOGIN_BUTTON)
        except:
            self.click(self.LOGIN_BUTTON_CSS)
        return self
    
    def login(self, email, password):
        """Perform admin login"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self):
        """Get error message"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_login_successful(self):
        """Check if login was successful"""
        try:
            self.wait_for_url_contains("/admin", timeout=10)
            return "login" not in self.get_current_url().lower()
        except:
            return False
