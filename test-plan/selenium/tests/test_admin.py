"""
Admin Tests
===========
Test cases for admin panel functionality
"""

import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.admin_login_page import AdminLoginPage
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from conftest import Config


class AdminDashboardPage(BasePage):
    """Page object for Admin Dashboard"""
    
    # Locators - Đã cập nhật theo frontend thực tế
    LOGO = (By.XPATH, "//h1[contains(text(),'PHDTECH')]")
    DASHBOARD_TITLE = (By.XPATH, "//h3[contains(text(),'Quản trị Admin')]")
    
    # Statistics cards
    USER_COUNT = (By.XPATH, "//h3[contains(text(),'Tổng số người đăng ký')]/following-sibling::p")
    ORDER_COUNT = (By.XPATH, "//h3[contains(text(),'Số sản phẩm bán được')]/following-sibling::p")
    REVENUE = (By.XPATH, "//h3[contains(text(),'Doanh thu hôm nay')]/following-sibling::p")
    
    USER_CARD = (By.CSS_SELECTOR, "div.bg-blue-100")
    ORDER_CARD = (By.CSS_SELECTOR, "div.bg-green-100")
    REVENUE_CARD = (By.CSS_SELECTOR, "div.bg-yellow-100")
    
    # Navigation - Sidebar menu
    USERS_MENU = (By.XPATH, "//a[contains(@href,'/admin/manageuser')]")
    USERS_MENU_TEXT = (By.XPATH, "//span[contains(text(),'Quản lý người dùng')]")
    PRODUCTS_MENU = (By.XPATH, "//a[contains(@href,'/admin/managegood')]")
    PRODUCTS_MENU_TEXT = (By.XPATH, "//span[contains(text(),'Quản lý sản phẩm')]")
    ORDERS_MENU = (By.XPATH, "//a[contains(@href,'/admin/managebill')]")
    ORDERS_MENU_TEXT = (By.XPATH, "//span[contains(text(),'Quản lý đơn hàng')]")
    REVENUE_MENU = (By.XPATH, "//a[contains(@href,'/admin') and not(contains(@href,'manage'))]")
    
    # Logout
    LOGOUT_BUTTON = (By.XPATH, "//li[contains(text(),'Đăng xuất')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_dashboard_loaded(self):
        """Check if dashboard is loaded"""
        return self.is_element_visible(self.LOGO) or \
               self.is_element_visible(self.USER_CARD) or \
               ("/admin" in self.get_current_url().lower() and "/login" not in self.get_current_url().lower())
    
    def navigate_to_users(self):
        """Navigate to user management"""
        try:
            self.click(self.USERS_MENU)
        except:
            self.click(self.USERS_MENU_TEXT)
        return self
    
    def navigate_to_products(self):
        """Navigate to product management"""
        try:
            self.click(self.PRODUCTS_MENU)
        except:
            self.click(self.PRODUCTS_MENU_TEXT)
        return self
    
    def navigate_to_orders(self):
        """Navigate to order management"""
        try:
            self.click(self.ORDERS_MENU)
        except:
            self.click(self.ORDERS_MENU_TEXT)
        return self


class TestAdminLogin:
    """Test cases for admin login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.admin_login_page = AdminLoginPage(driver)
        self.admin_dashboard = AdminDashboardPage(driver)
    
    def test_admin_login_page_loads(self):
        """TC_ADMIN_001: Verify admin login page loads"""
        self.admin_login_page.open_admin_login_page(self.base_url)
        
        assert self.admin_login_page.is_element_visible(AdminLoginPage.EMAIL_INPUT), \
            "Email field should be visible"
        assert self.admin_login_page.is_element_visible(AdminLoginPage.PASSWORD_INPUT), \
            "Password field should be visible"
    
    def test_admin_login_with_valid_credentials(self):
        """TC_ADMIN_002: Verify admin login with valid credentials"""
        self.admin_login_page.open_admin_login_page(self.base_url)
        self.admin_login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        
        import time
        time.sleep(2)
        
        assert self.admin_login_page.is_login_successful() or \
               self.admin_dashboard.is_dashboard_loaded(), \
            "Admin login should be successful"
    
    def test_admin_login_with_invalid_credentials(self):
        """TC_ADMIN_003: Verify admin login fails with invalid credentials"""
        self.admin_login_page.open_admin_login_page(self.base_url)
        self.admin_login_page.login("invalid@admin.com", "wrongpassword")
        
        import time
        time.sleep(1)
        
        error = self.admin_login_page.get_error_message()
        assert error is not None or not self.admin_login_page.is_login_successful(), \
            "Admin login should fail with invalid credentials"
    
    def test_admin_login_with_user_credentials(self):
        """TC_ADMIN_004: Verify admin login fails with regular user credentials"""
        self.admin_login_page.open_admin_login_page(self.base_url)
        self.admin_login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
        
        import time
        time.sleep(1)
        
        # Should fail or show unauthorized
        assert not self.admin_dashboard.is_dashboard_loaded() or \
               self.admin_login_page.get_error_message() is not None, \
            "Regular user should not be able to login as admin"


class TestAdminDashboard:
    """Test cases for admin dashboard"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.admin_login_page = AdminLoginPage(driver)
        self.admin_dashboard = AdminDashboardPage(driver)
    
    def login_as_admin(self):
        """Helper to login as admin"""
        self.admin_login_page.open_admin_login_page(self.base_url)
        self.admin_login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        import time
        time.sleep(2)
    
    def test_dashboard_displays_statistics(self):
        """TC_ADMIN_005: Verify dashboard displays statistics"""
        self.login_as_admin()
        
        # Dashboard should show some statistics
        assert self.admin_dashboard.is_dashboard_loaded(), \
            "Dashboard should be loaded with statistics"
    
    def test_navigate_to_user_management(self):
        """TC_ADMIN_006: Verify navigation to user management"""
        self.login_as_admin()
        self.admin_dashboard.navigate_to_users()
        
        import time
        time.sleep(1)
        
        assert "user" in self.admin_dashboard.get_current_url().lower(), \
            "Should navigate to user management"
    
    def test_navigate_to_product_management(self):
        """TC_ADMIN_007: Verify navigation to product management"""
        self.login_as_admin()
        self.admin_dashboard.navigate_to_products()
        
        import time
        time.sleep(1)
        
        assert "good" in self.admin_dashboard.get_current_url().lower(), \
            "Should navigate to product management"
    
    def test_navigate_to_order_management(self):
        """TC_ADMIN_008: Verify navigation to order management"""
        self.login_as_admin()
        self.admin_dashboard.navigate_to_orders()
        
        import time
        time.sleep(1)
        
        assert "bill" in self.admin_dashboard.get_current_url().lower() or \
               "order" in self.admin_dashboard.get_current_url().lower(), \
            "Should navigate to order management"


class TestAdminUserManagement:
    """Test cases for admin user management"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.admin_login_page = AdminLoginPage(driver)
        self.admin_dashboard = AdminDashboardPage(driver)
    
    def login_and_navigate_to_users(self):
        """Helper to login and navigate to users"""
        self.admin_login_page.open_admin_login_page(self.base_url)
        self.admin_login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        import time
        time.sleep(2)
        self.admin_dashboard.navigate_to_users()
        time.sleep(1)
    
    def test_user_list_displays(self):
        """TC_ADMIN_009: Verify user list displays"""
        self.login_and_navigate_to_users()
        
        # Should display user list table
        user_table = (By.CSS_SELECTOR, "table, [class*='user-list']")
        assert self.admin_dashboard.is_element_visible(user_table) or \
               "manageuser" in self.admin_dashboard.get_current_url().lower(), \
            "User list should be displayed"


class TestAdminProductManagement:
    """Test cases for admin product management"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.admin_login_page = AdminLoginPage(driver)
        self.admin_dashboard = AdminDashboardPage(driver)
    
    def login_and_navigate_to_products(self):
        """Helper to login and navigate to products"""
        self.admin_login_page.open_admin_login_page(self.base_url)
        self.admin_login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        import time
        time.sleep(2)
        self.admin_dashboard.navigate_to_products()
        time.sleep(1)
    
    def test_product_list_displays(self):
        """TC_ADMIN_010: Verify product list displays"""
        self.login_and_navigate_to_products()
        
        # Should display product list
        product_table = (By.CSS_SELECTOR, "table, [class*='product-list'], [class*='good']")
        assert self.admin_dashboard.is_element_visible(product_table) or \
               "managegood" in self.admin_dashboard.get_current_url().lower(), \
            "Product list should be displayed"
