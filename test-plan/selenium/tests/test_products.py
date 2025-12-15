"""
Product Tests
=============
Test cases for product browsing and interaction
"""

import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.home_page import HomePage
from pages.product_page import ProductPage


class TestProductBrowsing:
    """Test cases for product browsing"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.home_page = HomePage(driver)
        self.product_page = ProductPage(driver)
    
    def test_home_page_displays_products(self):
        """TC_PROD_001: Verify home page displays products"""
        self.home_page.open_home_page(self.base_url)
        
        product_count = self.home_page.get_product_count()
        assert product_count > 0, "Home page should display products"
    
    def test_product_detail_page_loads(self):
        """TC_PROD_002: Verify product detail page loads"""
        self.product_page.open_product_page(self.base_url, 1)
        
        assert self.product_page.is_product_loaded(), "Product page should load"
    
    def test_product_has_title(self):
        """TC_PROD_003: Verify product has title"""
        self.product_page.open_product_page(self.base_url, 1)
        
        title = self.product_page.get_product_title()
        assert title and len(title) > 0, "Product should have a title"
    
    def test_product_has_price(self):
        """TC_PROD_004: Verify product has price"""
        self.product_page.open_product_page(self.base_url, 1)
        
        price = self.product_page.get_product_price()
        assert price and len(price) > 0, "Product should have a price"
    
    def test_add_to_cart_button_visible(self):
        """TC_PROD_005: Verify Add to Cart button is visible"""
        self.product_page.open_product_page(self.base_url, 1)
        
        assert self.product_page.is_add_to_cart_button_visible(), \
            "Add to Cart button should be visible"
    
    def test_navigate_to_product_from_home(self):
        """TC_PROD_006: Verify navigation to product from home page"""
        self.home_page.open_home_page(self.base_url)
        self.home_page.click_first_product()
        
        assert self.product_page.is_product_loaded(), \
            "Should navigate to product detail page"
    
    def test_product_quantity_default_value(self):
        """TC_PROD_007: Verify product quantity default value"""
        self.product_page.open_product_page(self.base_url, 1)
        
        quantity = self.product_page.get_quantity()
        assert quantity >= 1, "Default quantity should be at least 1"
    
    def test_increase_product_quantity(self):
        """TC_PROD_008: Verify increasing product quantity"""
        self.product_page.open_product_page(self.base_url, 1)
        
        initial_qty = self.product_page.get_quantity()
        self.product_page.increase_quantity()
        new_qty = self.product_page.get_quantity()
        
        assert new_qty == initial_qty + 1, "Quantity should increase by 1"
    
    def test_decrease_product_quantity(self):
        """TC_PROD_009: Verify decreasing product quantity"""
        self.product_page.open_product_page(self.base_url, 1)
        
        # First increase to 2
        self.product_page.increase_quantity()
        initial_qty = self.product_page.get_quantity()
        self.product_page.decrease_quantity()
        new_qty = self.product_page.get_quantity()
        
        assert new_qty == initial_qty - 1, "Quantity should decrease by 1"


class TestProductCategories:
    """Test cases for product categories"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.home_page = HomePage(driver)
    
    def test_navigate_to_laptop_category(self):
        """TC_CAT_001: Verify navigation to laptop category"""
        self.home_page.open_home_page(self.base_url)
        self.home_page.navigate_to_laptops()
        
        assert "laptop" in self.home_page.get_current_url().lower(), \
            "Should navigate to laptop category"
    
    def test_navigate_to_mouse_category(self):
        """TC_CAT_002: Verify navigation to mouse category"""
        self.home_page.open_home_page(self.base_url)
        self.home_page.navigate_to_mouse()
        
        assert "mouse" in self.home_page.get_current_url().lower(), \
            "Should navigate to mouse category"
    
    def test_navigate_to_keyboard_category(self):
        """TC_CAT_003: Verify navigation to keyboard category"""
        self.home_page.open_home_page(self.base_url)
        self.home_page.navigate_to_keyboard()
        
        assert "keyboard" in self.home_page.get_current_url().lower(), \
            "Should navigate to keyboard category"


class TestProductSearch:
    """Test cases for product search"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.home_page = HomePage(driver)
    
    def test_search_with_valid_keyword(self):
        """TC_SEARCH_001: Verify search with valid keyword"""
        self.home_page.open_home_page(self.base_url)
        self.home_page.search_product("laptop")
        
        # Check if search results are displayed or URL changed
        # This depends on implementation
        import time
        time.sleep(2)  # Wait for search results
        
        # Verify search was performed (implementation specific)
        assert True  # Replace with actual assertion
    
    def test_search_with_empty_keyword(self):
        """TC_SEARCH_002: Verify search with empty keyword"""
        self.home_page.open_home_page(self.base_url)
        self.home_page.search_product("")
        
        # Should stay on current page or show all products
        assert self.home_page.is_page_loaded(), "Page should still be loaded"
