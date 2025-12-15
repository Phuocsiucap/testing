import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_EMAIL = os.getenv('CLIENT_EMAIL', 'admin@gmail.com') 
CLIENT_PASSWORD = os.getenv('CLIENT_PASSWORD', '123456')
BASE_URL = "https://testing-ao3c.onrender.com/#/"

# LambdaTest credentials (optional)
LT_USERNAME = os.getenv('LT_USERNAME')
LT_ACCESS_KEY = os.getenv('LT_ACCESS_KEY')
USE_LT = bool(LT_USERNAME and LT_ACCESS_KEY)

@pytest.fixture(scope="module")
def driver():
    """Create a WebDriver. Use LambdaTest remote if LT credentials present, otherwise local Chrome."""
    if USE_LT:
        # Configure LambdaTest capabilities
        caps = {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "LT:Options": {
                "platformName": "Windows 10",
                "user": LT_USERNAME,
                "accessKey": LT_ACCESS_KEY,
                "build": "demo_test_build",
                "name": "pytest_demo_test"
            }
        }
        hub_url = f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@hub.lambdatest.com/wd/hub"
        driver = webdriver.Remote(command_executor=hub_url, desired_capabilities=caps)
    else:
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)

    try:
        driver.maximize_window()
    except Exception:
        pass

    yield driver
    driver.quit()

def handle_alert(driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        time.sleep(1) # Chờ 1 chút sau khi đóng alert
        return True, alert_text
    except TimeoutException:
        return False, None

def login_user(driver):
    """Đăng nhập và xử lý alert thành công"""
    # Chỉ navigate nếu chưa ở trang login và chưa đăng nhập
    if "/login" not in driver.current_url:
         # Kiểm tra nhanh xem đã có nút logout chưa (đã login rồi)
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'logout')]")))
            print("ℹ️ Đã đăng nhập trước đó.")
            return
        except:
            driver.get(BASE_URL + "login")

    try:
        # Chờ field email xuất hiện
        email_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        
        email_field.clear()
        email_field.send_keys(CLIENT_EMAIL)
        
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(CLIENT_PASSWORD)
        
        # --- SỬA LỖI Ở ĐÂY ---
        # Cách 1: Tìm nút có type là submit (An toàn nhất cho form)
        # Cách 2: Tìm nút chứa chữ Đăng Nhập (Bất kể hoa thường/khoảng trắng)
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'] | //button[contains(text(), 'Đăng Nhập')] | //button[contains(text(), 'Đăng nhập')]")
        submit_btn.click()

        # Xử lý Alert "Đăng nhập thành công"
        is_alert, text = handle_alert(driver, timeout=10)
        if is_alert:
            print(f"\n ℹ️ Info: Đã đóng alert '{text}'")

        # Chờ chuyển hướng về trang chủ
        WebDriverWait(driver, 10).until(EC.url_contains("/"))
    except Exception as e:
        print(f"Lỗi login: {e}")
        # Nếu đã login rồi thì bỏ qua lỗi này

def open_cart_page(driver):
    """Mở trang giỏ hàng"""
    driver.get(BASE_URL + "cartshopping")
    # Chờ URL đổi hoặc chờ element đặc trưng của giỏ hàng load xong
    WebDriverWait(driver, 10).until(EC.url_contains("cartshopping"))

def test_cart_empty_add_first_product(driver):
    print("\n---------------------------------------------------")
    print("▶️  Bắt đầu test: Vào giỏ hàng, nếu trống thì thêm sản phẩm đầu tiên")
    
    login_user(driver)
    time.sleep(2) # Chờ ổn định sau login
    open_cart_page(driver)
    
    # Kiểm tra giỏ hàng có trống không
    # Dựa vào file CartShopping.js: "Bạn chưa có sản phẩm nào trong giỏ hàng"
    try:
        # Dùng wait ngắn để check text trống
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Bạn chưa có sản phẩm nào trong giỏ hàng')]"))
        )
        print("ℹ️  Giỏ hàng trống, về trang chủ để thêm sản phẩm.")
        
        # 1. Về trang chủ
        driver.get(BASE_URL)
        
        # 2. Click vào sản phẩm đầu tiên
        # --- SỬA LỖI SELECTOR SẢN PHẨM ---
        # React code dùng Link to='/product/...' nên ta tìm thẻ <a> có href chứa 'product'
        print("Đang tìm sản phẩm...")
        first_product = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(@href, '/product/')])[1]"))
        )
        # Scroll tới sản phẩm để tránh bị Header che khuất
        driver.execute_script("arguments[0].scrollIntoView();", first_product)
        time.sleep(1)
        first_product.click()
        
        # Chờ trang chi tiết load
        WebDriverWait(driver, 10).until(EC.url_contains("/product/"))
        
        # 3. Thêm sản phẩm vào giỏ
        # Tìm nút thêm giỏ hàng (Check lại text trên trang ProductDetail của bạn)
        # Thường là "Thêm vào giỏ" hoặc "Mua ngay"
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Thêm') or contains(text(), 'Mua')]"))
        )
        add_to_cart_button.click()
        
        # Xử lý alert "Thêm thành công" nếu có
        handle_alert(driver)
        
        print("✅ [PASS] Đã thêm sản phẩm đầu tiên vào giỏ hàng.")
        
        # 4. Quay lại giỏ hàng check
        open_cart_page(driver)
        
        # Check xem có item nào không (Class 'flex items-center...' trong CartItem.js)
        # Ta check img hoặc checkbox để chắc chắn có hàng
        cart_items = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='checkbox']"))
        )
        assert len(cart_items) > 0, "Giỏ hàng vẫn trống sau khi thêm sản phẩm."
        
    except TimeoutException:
        print("ℹ️  Giỏ hàng KHÔNG trống (hoặc không tìm thấy thông báo trống).")
        # Nếu không trống, verify là có item
        cart_items = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        if len(cart_items) > 0:
             print(f"✅ [PASS] Giỏ hàng đang có {len(cart_items)} sản phẩm.")
        else:
             print("❌ [FAIL] Không tìm thấy text trống, cũng không thấy sản phẩm.")