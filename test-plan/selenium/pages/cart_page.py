"""
Cart Page Object
================
Page object for shopping cart page
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    """Page object for Shopping Cart page"""
    
    # Locators - Đã cập nhật theo frontend thực tế
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[contains(text(),'Bạn chưa có sản phẩm nào trong giỏ hàng')]")
    NOT_LOGGED_IN_MESSAGE = (By.XPATH, "//*[contains(text(),'Bạn chưa đăng nhập')]")
    LOGIN_LINK_IN_CART = (By.XPATH, "//a[contains(@href,'/login') and contains(text(),'Đăng nhập ngay')]")
    
    # Cart items
    CART_ITEMS = (By.CSS_SELECTOR, "div.flex.items-center.bg-white.shadow-sm, .cart-item")
    ITEM_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    ITEM_NAME = (By.CSS_SELECTOR, "p.font-semibold")
    ITEM_PRICE = (By.CSS_SELECTOR, "p.text-red-500.font-semibold")
    ITEM_IMAGE = (By.CSS_SELECTOR, "img")
    
    # Quantity controls  
    QUANTITY_DISPLAY = (By.XPATH, "//p[contains(text(),'Số lượng')]")
    INCREASE_QUANTITY = (By.CSS_SELECTOR, "svg.HiPlusSm, [class*='HiPlusSm']")
    DECREASE_QUANTITY = (By.CSS_SELECTOR, "svg.RiSubtractFill, [class*='RiSubtractFill']")
    REMOVE_ITEM = (By.XPATH, "//span[contains(text(),'Xóa') and contains(@class,'text-red-500')]")
    
    # Buttons
    SELECT_ALL_BUTTON = (By.XPATH, "//button[contains(text(),'Chọn tất cả') or contains(text(),'Bỏ chọn tất cả')]")
    SELECT_ALL_CSS = (By.CSS_SELECTOR, "button.bg-blue-500")
    
    # Voucher
    USE_VOUCHER_BUTTON = (By.XPATH, "//button[contains(text(),'Sử dụng Voucher') or contains(text(),'voucher')]")
    
    # Checkout
    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(),'Đặt hàng')]")
    CHECKOUT_CSS = (By.CSS_SELECTOR, "button.bg-primary, button.bg-red-500")
    
    # Total
    TOTAL_PRICE = (By.XPATH, "//*[contains(text(),'Tổng tiền') or contains(text(),'Tổng cộng')]")
    
    # Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, [class*='success']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, [class*='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/#/cartshopping"
    
    def open_cart_page(self, base_url):
        """Navigate to cart page"""
        self.open(f"{base_url}{self.url}")
        self.wait_for_page_load()
        return self
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=3) or self.get_item_count() == 0
    
    def get_item_count(self):
        """Get number of items in cart"""
        return len(self.find_elements(self.CART_ITEMS))
    
    def get_item_names(self):
        """Get names of all items in cart"""
        elements = self.find_elements(self.ITEM_NAME)
        return [el.text for el in elements if el.text]
    
    def get_cart_total(self):
        """Get cart total"""
        if self.is_element_present(self.TOTAL):
            return self.get_text(self.TOTAL)
        return "0"
    
    def update_item_quantity(self, item_index, quantity):
        """Update quantity for specific item"""
        quantity_inputs = self.find_elements(self.ITEM_QUANTITY)
        if quantity_inputs and item_index < len(quantity_inputs):
            quantity_inputs[item_index].clear()
            quantity_inputs[item_index].send_keys(str(quantity))
        return self
    
    def remove_item(self, item_index=0):
        """Remove item from cart"""
        remove_buttons = self.find_elements(self.REMOVE_ITEM)
        if remove_buttons and item_index < len(remove_buttons):
            remove_buttons[item_index].click()
        return self
    
    def remove_all_items(self):
        """Remove all items from cart"""
        while self.get_item_count() > 0:
            self.remove_item(0)
            import time
            time.sleep(0.5)
        return self
    
    def apply_voucher(self, voucher_code):
        """Apply voucher code"""
        self.type_text(self.VOUCHER_INPUT, voucher_code)
        self.click(self.APPLY_VOUCHER_BUTTON)
        return self
    
    def click_checkout(self):
        """Click checkout button"""
        self.click(self.CHECKOUT_BUTTON)
        return self
    
    def click_continue_shopping(self):
        """Click continue shopping link"""
        self.click(self.CONTINUE_SHOPPING_LINK)
        return self
    
    def is_checkout_button_visible(self):
        """Check if checkout button is visible"""
        return self.is_element_visible(self.CHECKOUT_BUTTON)
    
    def get_success_message(self):
        """Get success message"""
        if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=3):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def get_error_message(self):
        """Get error message"""
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        return None
