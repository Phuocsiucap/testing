"""
Register Page Object
====================
Page object for user registration functionality
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class RegisterPage(BasePage):
    """Page object for Registration page"""
    
    # Locators - Đã cập nhật theo frontend thực tế
    USERNAME_INPUT = (By.CSS_SELECTOR, "input#name, input[name='name']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#email, input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#password, input[name='password']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input#confirmpassword, input[name='confirmpassword']")
    REGISTER_BUTTON = (By.XPATH, "//button[contains(text(),'Đăng ký')]")
    REGISTER_BUTTON_CSS = (By.CSS_SELECTOR, "button.bg-primary")
    LOGIN_LINK = (By.XPATH, "//a[contains(@href,'/login') or contains(text(),'Đăng nhập')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.text-red-500, .text-red-500")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .success-message, [class*='success'], .text-green-500")
    PAGE_TITLE = (By.XPATH, "//p[contains(text(),'Đăng ký')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/#/regester"
    
    def open_register_page(self, base_url):
        """Navigate to registration page"""
        self.open(f"{base_url}{self.url}")
        self.wait_for_page_load()
        return self
    
    def enter_username(self, username):
        """Enter username"""
        self.type_text(self.USERNAME_INPUT, username)
        return self
    
    def enter_email(self, email):
        """Enter email address"""
        self.type_text(self.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password):
        """Enter password"""
        self.type_text(self.PASSWORD_INPUT, password)
        return self
    
    def enter_confirm_password(self, password):
        """Enter confirm password"""
        if self.is_element_present(self.CONFIRM_PASSWORD_INPUT):
            self.type_text(self.CONFIRM_PASSWORD_INPUT, password)
        return self
    
    def click_register_button(self):
        """Click register button"""
        try:
            self.click(self.REGISTER_BUTTON)
        except:
            self.click(self.REGISTER_BUTTON_CSS)
        return self
    
    def register(self, username, email, password):
        """Complete registration with given details"""
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.click_register_button()
        return self
    
    def get_error_message(self):
        """Get error message if registration fails"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def get_success_message(self):
        """Get success message"""
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def is_registration_successful(self):
        """Check if registration was successful"""
        try:
            # Check for success message or redirect to login
            return self.is_element_visible(self.SUCCESS_MESSAGE) or "login" in self.get_current_url().lower()
        except:
            return False
    
    def click_login_link(self):
        """Click on login link"""
        self.click(self.LOGIN_LINK)
        return self
