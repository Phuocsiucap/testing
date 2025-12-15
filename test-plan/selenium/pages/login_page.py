"""
Login Page Object
=================
Page object for user login functionality
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for Login page"""
    
    # Locators - Đã cập nhật theo frontend thực tế
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#email, input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#password, input[name='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Đăng nhập')]")
    LOGIN_BUTTON_CSS = (By.CSS_SELECTOR, "button.bg-primary")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.text-red-500, .text-red-500")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .success-message, [class*='success']")
    REGISTER_LINK = (By.XPATH, "//a[contains(@href,'/regester') or contains(text(),'Đăng ký')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(),'Quên mật khẩu') or contains(text(),'Forgot')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/#/login"
    
    def open_login_page(self, base_url):
        """Navigate to login page"""
        self.open(f"{base_url}{self.url}")
        self.wait_for_page_load()
        return self
    
    def enter_email(self, email):
        """Enter email address"""
        self.type_text(self.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password):
        """Enter password"""
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
        """Perform login with given credentials"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self):
        """Get error message if login fails"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_login_successful(self):
        """Check if login was successful by checking URL change"""
        try:
            self.wait_for_url_contains("/", timeout=10)
            return "login" not in self.get_current_url().lower()
        except:
            return False
    
    def click_register_link(self):
        """Click on register link"""
        self.click(self.REGISTER_LINK)
        return self
    
    def click_forgot_password_link(self):
        """Click on forgot password link"""
        self.click(self.FORGOT_PASSWORD_LINK)
        return self
    
    def is_email_field_visible(self):
        """Check if email field is visible"""
        return self.is_element_visible(self.EMAIL_INPUT)
    
    def is_password_field_visible(self):
        """Check if password field is visible"""
        return self.is_element_visible(self.PASSWORD_INPUT)
    
    def is_login_button_visible(self):
        """Check if login button is visible"""
        return self.is_element_visible(self.LOGIN_BUTTON) or self.is_element_visible(self.LOGIN_BUTTON_CSS)
