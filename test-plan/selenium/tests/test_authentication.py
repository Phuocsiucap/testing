"""
Authentication Tests
====================
Test cases for user authentication (login, register, logout)
"""

import pytest
from faker import Faker
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.home_page import HomePage

fake = Faker()


class TestUserLogin:
    """Test cases for user login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
    
    def test_login_page_loads(self):
        """TC_AUTH_001: Verify login page loads correctly"""
        self.login_page.open_login_page(self.base_url)
        
        assert self.login_page.is_email_field_visible(), "Email field should be visible"
        assert self.login_page.is_password_field_visible(), "Password field should be visible"
        assert self.login_page.is_login_button_visible(), "Login button should be visible"
    
    def test_login_with_valid_credentials(self):
        """TC_AUTH_002: Verify login with valid credentials"""
        self.login_page.open_login_page(self.base_url)
        self.login_page.login("testuser@example.com", "Test@123456")
        
        # Wait and check for successful login
        assert self.login_page.is_login_successful(), "Login should be successful"
    
    def test_login_with_invalid_email(self):
        """TC_AUTH_003: Verify login fails with invalid email"""
        self.login_page.open_login_page(self.base_url)
        self.login_page.login("invalid@email.com", "Test@123456")
        
        error = self.login_page.get_error_message()
        assert error is not None or not self.login_page.is_login_successful(), \
            "Login should fail with invalid email"
    
    def test_login_with_wrong_password(self):
        """TC_AUTH_004: Verify login fails with wrong password"""
        self.login_page.open_login_page(self.base_url)
        self.login_page.login("testuser@example.com", "wrongpassword")
        
        error = self.login_page.get_error_message()
        assert error is not None or not self.login_page.is_login_successful(), \
            "Login should fail with wrong password"
    
    def test_login_with_empty_email(self):
        """TC_AUTH_005: Verify login fails with empty email"""
        self.login_page.open_login_page(self.base_url)
        self.login_page.enter_password("Test@123456")
        self.login_page.click_login_button()
        
        # Should show validation error or stay on login page
        assert "login" in self.login_page.get_current_url().lower(), \
            "Should stay on login page with empty email"
    
    def test_login_with_empty_password(self):
        """TC_AUTH_006: Verify login fails with empty password"""
        self.login_page.open_login_page(self.base_url)
        self.login_page.enter_email("testuser@example.com")
        self.login_page.click_login_button()
        
        # Should show validation error or stay on login page
        assert "login" in self.login_page.get_current_url().lower(), \
            "Should stay on login page with empty password"
    
    def test_navigate_to_register_from_login(self):
        """TC_AUTH_007: Verify navigation to register page from login"""
        self.login_page.open_login_page(self.base_url)
        self.login_page.click_register_link()
        
        assert "regester" in self.login_page.get_current_url().lower() or \
               "register" in self.login_page.get_current_url().lower(), \
            "Should navigate to register page"


class TestUserRegistration:
    """Test cases for user registration functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.register_page = RegisterPage(driver)
    
    def test_register_page_loads(self):
        """TC_REG_001: Verify register page loads correctly"""
        self.register_page.open_register_page(self.base_url)
        
        assert self.register_page.is_element_visible(RegisterPage.EMAIL_INPUT), \
            "Email field should be visible"
        assert self.register_page.is_element_visible(RegisterPage.PASSWORD_INPUT), \
            "Password field should be visible"
    
    def test_register_with_valid_data(self):
        """TC_REG_002: Verify registration with valid data"""
        self.register_page.open_register_page(self.base_url)
        
        # Generate unique test data
        username = fake.user_name()[:10]  # Tên tối thiểu 5 ký tự
        email = fake.email()
        password = "Test@12345678"  # Mật khẩu tối thiểu 8 ký tự
        
        self.register_page.register(username, email, password)
        
        import time
        time.sleep(2)
        
        # Check for success or redirect to login
        assert self.register_page.is_registration_successful() or \
               self.register_page.get_success_message() is not None or \
               "login" in self.register_page.get_current_url().lower(), \
            "Registration should be successful"
    
    def test_register_with_existing_email(self):
        """TC_REG_003: Verify registration fails with existing email"""
        self.register_page.open_register_page(self.base_url)
        
        self.register_page.register(
            "existinguser",
            "test@gmail.com",  # Assuming this email exists
            "Test@12345678"
        )
        
        import time
        time.sleep(1)
        
        error = self.register_page.get_error_message()
        assert error is not None or not self.register_page.is_registration_successful(), \
            "Registration should fail with existing email"
    
    def test_register_with_invalid_email_format(self):
        """TC_REG_004: Verify registration fails with invalid email format"""
        self.register_page.open_register_page(self.base_url)
        
        self.register_page.register(
            "testuser123",
            "invalidemail",  # Invalid email format
            "Test@12345678"
        )
        
        import time
        time.sleep(1)
        
        # Should show validation error
        error = self.register_page.get_error_message()
        assert error is not None or not self.register_page.is_registration_successful(), \
            "Registration should fail with invalid email format"
    
    def test_navigate_to_login_from_register(self):
        """TC_REG_005: Verify navigation to login page from register"""
        self.register_page.open_register_page(self.base_url)
        self.register_page.click_login_link()
        
        assert "login" in self.register_page.get_current_url().lower(), \
            "Should navigate to login page"


class TestUserLogout:
    """Test cases for user logout functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.home_page = HomePage(driver)
        self.login_page = LoginPage(driver)
    
    def test_logout_redirects_to_home(self, logged_in_driver):
        """TC_LOGOUT_001: Verify logout redirects user appropriately"""
        self.home_page.open_home_page(self.base_url)
        
        if self.home_page.is_user_logged_in():
            self.home_page.logout()
            
            # Should be logged out
            assert not self.home_page.is_user_logged_in() or \
                   "login" in self.home_page.get_current_url().lower(), \
                "User should be logged out"
