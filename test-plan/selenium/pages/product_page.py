"""
Product Page Object
===================
Page object for product detail page
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    """Page object for Product Detail page"""
    
    # Locators - Đã cập nhật theo frontend thực tế
    PRODUCT_TITLE = (By.CSS_SELECTOR, "p.font-bold.top-menu-item, .product-title, h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "p.text-red-500, .price, [class*='price']")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "div.group img, .product-image img")
    PRODUCT_COLOR = (By.XPATH, "//p[contains(text(),'Màu sắc')]")
    PRODUCT_STOCK = (By.XPATH, "//p[contains(text(),'Sản phẩm sẵn có')]")
    
    # Quantity controls
    QUANTITY_DISPLAY = (By.XPATH, "//p[contains(text(),'Số lượng')]/following-sibling::*")
    QUANTITY_INCREASE = (By.CSS_SELECTOR, "svg.HiPlusSm, [class*='HiPlusSm']")
    QUANTITY_INCREASE_XPATH = (By.XPATH, "//*[contains(@class,'HiPlusSm') or contains(@class,'plus')]")
    QUANTITY_DECREASE = (By.CSS_SELECTOR, "svg.RiSubtractFill, [class*='RiSubtractFill']")
    QUANTITY_DECREASE_XPATH = (By.XPATH, "//*[contains(@class,'RiSubtractFill') or contains(@class,'subtract')]")
    
    # Buttons
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(text(),'Thêm vào giỏ hàng')]")
    ADD_TO_CART_CSS = (By.CSS_SELECTOR, "button.bg-red-500")
    BUY_NOW_BUTTON = (By.XPATH, "//button[contains(text(),'Mua ngay')]")
    BUY_NOW_CSS = (By.CSS_SELECTOR, "button.bg-yellow-400")
    
    # Sale information
    SALE_BADGE = (By.CSS_SELECTOR, "p.bg-primary, .sale-badge")
    PROMOTION_LIST = (By.CSS_SELECTOR, "div.bg-green-50 li")
    
    # Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, [class*='success'], .toast-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, [class*='error'], .toast-error")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_product_page(self, base_url, product_id):
        """Navigate to product detail page"""
        self.open(f"{base_url}/#/product/{product_id}")
        self.wait_for_page_load()
        return self
    
    def get_product_title(self):
        """Get product title"""
        return self.get_text(self.PRODUCT_TITLE)
    
    def get_product_price(self):
        """Get product price"""
        return self.get_text(self.PRODUCT_PRICE)
    
    def get_product_description(self):
        """Get product description"""
        if self.is_element_present(self.PRODUCT_DESCRIPTION):
            return self.get_text(self.PRODUCT_DESCRIPTION)
        return ""
    
    def get_quantity(self):
        """Get current quantity value"""
        return int(self.get_attribute(self.QUANTITY_INPUT, "value") or 1)
    
    def set_quantity(self, quantity):
        """Set product quantity"""
        self.type_text(self.QUANTITY_INPUT, str(quantity))
        return self
    
    def increase_quantity(self, times=1):
        """Increase quantity"""
        for _ in range(times):
            self.click(self.QUANTITY_INCREASE)
        return self
    
    def decrease_quantity(self, times=1):
        """Decrease quantity"""
        for _ in range(times):
            self.click(self.QUANTITY_DECREASE)
        return self
    
    def click_add_to_cart(self):
        """Click Add to Cart button"""
        self.click(self.ADD_TO_CART_BUTTON)
        return self
    
    def click_buy_now(self):
        """Click Buy Now button"""
        self.click(self.BUY_NOW_BUTTON)
        return self
    
    def is_add_to_cart_button_visible(self):
        """Check if Add to Cart button is visible"""
        return self.is_element_visible(self.ADD_TO_CART_BUTTON)
    
    def is_product_loaded(self):
        """Check if product page is loaded"""
        return self.is_element_visible(self.PRODUCT_TITLE)
    
    def get_success_message(self):
        """Get success message after adding to cart"""
        if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def get_error_message(self):
        """Get error message"""
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_in_stock(self):
        """Check if product is in stock"""
        if self.is_element_present(self.STOCK_STATUS):
            stock_text = self.get_text(self.STOCK_STATUS).lower()
            return "hết hàng" not in stock_text and "out of stock" not in stock_text
        return True  # Assume in stock if no status shown
    
    def get_image_count(self):
        """Get number of product images"""
        return len(self.find_elements(self.PRODUCT_IMAGES))
