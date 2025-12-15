"""
Home Page Object
================
Page object for main home page
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """Page object for Home page"""
    
    # Locators - Đã cập nhật theo frontend thực tế
    HEADER = (By.CSS_SELECTOR, "div.container, nav")
    LOGO = (By.XPATH, "//a[contains(text(),'PhdTech') or contains(text(),'PHDTECH')]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.input-search, input[placeholder*='Tìm kiếm']")
    CART_ICON = (By.XPATH, "//a[@href='/cartshopping']")
    CART_ICON_SVG = (By.CSS_SELECTOR, "svg.FaShoppingCart, a[href='/cartshopping']")
    LOGIN_LINK = (By.XPATH, "//a[contains(@href,'login') or contains(text(),'Đăng Nhập')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(@href,'regester') or contains(text(),'Đăng Ký')]")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "a.bg-primary[href='/regester']")
    USER_ICON = (By.XPATH, "//a[contains(@href,'profile')]")
    SALE_BUTTON = (By.XPATH, "//a[contains(@href,'saleproduct') or contains(text(),'Sale')]")
    
    # Navigation menu
    LAPTOP_LINK = (By.XPATH, "//a[contains(@href,'/laptop') or contains(text(),'Máy tính')]")
    MOUSE_LINK = (By.XPATH, "//a[contains(@href,'/mouse') or contains(text(),'Chuột')]")
    KEYBOARD_LINK = (By.XPATH, "//a[contains(@href,'/keyboard') or contains(text(),'Bàn Phím')]")
    ABOUT_LINK = (By.XPATH, "//a[contains(@href,'/about') or contains(text(),'Về chúng tôi')]")
    
    # Product elements
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card, [class*='product'], .card, a[href*='/product/']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-name, .product-title, h3, h4")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-price, .price, [class*='price'], .text-red-500")
    
    # Footer
    FOOTER = (By.CSS_SELECTOR, "footer, .footer")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/"
    
    def open_home_page(self, base_url):
        """Navigate to home page"""
        self.open(base_url)
        self.wait_for_page_load()
        return self
    
    def is_page_loaded(self):
        """Check if home page is loaded"""
        return self.is_element_visible(self.HEADER)
    
    def search_product(self, keyword):
        """Search for a product"""
        self.type_text(self.SEARCH_INPUT, keyword)
        if self.is_element_present(self.SEARCH_BUTTON):
            self.click(self.SEARCH_BUTTON)
        return self
    
    def click_cart_icon(self):
        """Click on cart icon"""
        self.click(self.CART_ICON)
        return self
    
    def click_login_link(self):
        """Click on login link"""
        self.click(self.LOGIN_LINK)
        return self
    
    def click_register_link(self):
        """Click on register link"""
        self.click(self.REGISTER_LINK)
        return self
    
    def click_profile_link(self):
        """Click on profile link"""
        if self.is_element_present(self.USER_MENU):
            self.click(self.USER_MENU)
        self.click(self.PROFILE_LINK)
        return self
    
    def logout(self):
        """Logout current user"""
        if self.is_element_present(self.USER_MENU):
            self.click(self.USER_MENU)
        self.click(self.LOGOUT_BUTTON)
        return self
    
    def get_product_count(self):
        """Get number of products displayed"""
        return len(self.find_elements(self.PRODUCT_CARDS))
    
    def click_first_product(self):
        """Click on first product"""
        products = self.find_elements(self.PRODUCT_CARDS)
        if products:
            products[0].click()
        return self
    
    def click_product_by_index(self, index):
        """Click on product by index"""
        products = self.find_elements(self.PRODUCT_CARDS)
        if products and index < len(products):
            products[index].click()
        return self
    
    def navigate_to_laptops(self):
        """Navigate to laptop category"""
        self.click(self.LAPTOP_LINK)
        return self
    
    def navigate_to_mouse(self):
        """Navigate to mouse category"""
        self.click(self.MOUSE_LINK)
        return self
    
    def navigate_to_keyboard(self):
        """Navigate to keyboard category"""
        self.click(self.KEYBOARD_LINK)
        return self
    
    def is_user_logged_in(self):
        """Check if user is logged in"""
        return self.is_element_present(self.USER_MENU) or self.is_element_present(self.PROFILE_LINK)
    
    def get_product_names(self):
        """Get all product names"""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements if el.text]
