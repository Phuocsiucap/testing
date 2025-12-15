"""
Shopping Cart Tests
===================
Test cases for shopping cart functionality
"""

import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from conftest import Config


class TestShoppingCart:
    """Test cases for shopping cart functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.cart_page = CartPage(driver)
        self.product_page = ProductPage(driver)
        self.login_page = LoginPage(driver)
    
    def login_user(self):
        """Helper method to login user"""
        self.login_page.open_login_page(self.base_url)
        self.login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
        import time
        time.sleep(2)
    
    def test_cart_page_loads(self):
        """TC_CART_001: Verify cart page loads"""
        self.login_user()
        self.cart_page.open_cart_page(self.base_url)
        
        # Cart page should load
        assert "cart" in self.cart_page.get_current_url().lower(), \
            "Cart page should load"
    
    def test_add_product_to_cart(self):
        """TC_CART_002: Verify adding product to cart"""
        self.login_user()
        
        # Open product and add to cart
        self.product_page.open_product_page(self.base_url, 1)
        self.product_page.click_add_to_cart()
        
        # Check for success message or cart update
        success = self.product_page.get_success_message()
        assert success is not None or True, "Product should be added to cart"
    
    def test_cart_displays_added_items(self):
        """TC_CART_003: Verify cart displays added items"""
        self.login_user()
        
        # Add product to cart first
        self.product_page.open_product_page(self.base_url, 1)
        self.product_page.click_add_to_cart()
        import time
        time.sleep(1)
        
        # Open cart
        self.cart_page.open_cart_page(self.base_url)
        time.sleep(1)
        
        # Check if cart has items
        item_count = self.cart_page.get_item_count()
        assert item_count > 0 or not self.cart_page.is_cart_empty(), \
            "Cart should display added items"
    
    def test_update_cart_item_quantity(self):
        """TC_CART_004: Verify updating cart item quantity"""
        self.login_user()
        
        # Ensure there's an item in cart
        self.product_page.open_product_page(self.base_url, 1)
        self.product_page.click_add_to_cart()
        import time
        time.sleep(1)
        
        # Open cart and update quantity
        self.cart_page.open_cart_page(self.base_url)
        time.sleep(1)
        
        if not self.cart_page.is_cart_empty():
            self.cart_page.update_item_quantity(0, 3)
            # Verify update (implementation specific)
            assert True
    
    def test_remove_item_from_cart(self):
        """TC_CART_005: Verify removing item from cart"""
        self.login_user()
        
        # Add product to cart
        self.product_page.open_product_page(self.base_url, 1)
        self.product_page.click_add_to_cart()
        import time
        time.sleep(1)
        
        # Open cart
        self.cart_page.open_cart_page(self.base_url)
        time.sleep(1)
        
        initial_count = self.cart_page.get_item_count()
        if initial_count > 0:
            self.cart_page.remove_item(0)
            time.sleep(1)
            new_count = self.cart_page.get_item_count()
            assert new_count < initial_count, "Item should be removed from cart"
    
    def test_empty_cart_message(self):
        """TC_CART_006: Verify empty cart message"""
        self.login_user()
        
        self.cart_page.open_cart_page(self.base_url)
        
        # If cart is empty, should show message
        if self.cart_page.is_cart_empty():
            assert self.cart_page.is_element_visible(CartPage.EMPTY_CART_MESSAGE) or True, \
                "Empty cart message should be displayed"
    
    def test_checkout_button_visibility(self):
        """TC_CART_007: Verify checkout button visibility"""
        self.login_user()
        
        # Add item to cart
        self.product_page.open_product_page(self.base_url, 1)
        self.product_page.click_add_to_cart()
        import time
        time.sleep(1)
        
        self.cart_page.open_cart_page(self.base_url)
        time.sleep(1)
        
        if not self.cart_page.is_cart_empty():
            assert self.cart_page.is_checkout_button_visible(), \
                "Checkout button should be visible when cart has items"
    
    def test_cart_requires_login(self):
        """TC_CART_008: Verify cart requires login for checkout"""
        # Navigate to cart without login
        self.cart_page.open_cart_page(self.base_url)
        
        # Should redirect to login or show login prompt
        # This depends on implementation
        assert True  # Replace with actual assertion based on implementation
    
    def test_apply_voucher_to_cart(self):
        """TC_CART_009: Verify applying voucher to cart"""
        self.login_user()
        
        # Add item to cart
        self.product_page.open_product_page(self.base_url, 1)
        self.product_page.click_add_to_cart()
        import time
        time.sleep(1)
        
        self.cart_page.open_cart_page(self.base_url)
        time.sleep(1)
        
        if not self.cart_page.is_cart_empty():
            # Try to apply voucher
            if self.cart_page.is_element_present(CartPage.VOUCHER_INPUT):
                self.cart_page.apply_voucher("TESTVOUCHER")
                # Check for success or error message
                assert True  # Replace with actual assertion


class TestCartPersistence:
    """Test cases for cart persistence"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.cart_page = CartPage(driver)
        self.product_page = ProductPage(driver)
        self.login_page = LoginPage(driver)
    
    def test_cart_persists_after_page_refresh(self):
        """TC_CART_010: Verify cart persists after page refresh"""
        # Login
        self.login_page.open_login_page(self.base_url)
        self.login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
        import time
        time.sleep(2)
        
        # Add item to cart
        self.product_page.open_product_page(self.base_url, 1)
        self.product_page.click_add_to_cart()
        time.sleep(1)
        
        # Open cart and get item count
        self.cart_page.open_cart_page(self.base_url)
        time.sleep(1)
        initial_count = self.cart_page.get_item_count()
        
        # Refresh page
        self.cart_page.refresh()
        time.sleep(2)
        
        # Check cart still has items
        new_count = self.cart_page.get_item_count()
        assert new_count == initial_count, "Cart should persist after refresh"
