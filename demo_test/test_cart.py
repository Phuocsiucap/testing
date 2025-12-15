import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, StaleElementReferenceException
import time
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_EMAIL = os.getenv('CLIENT_EMAIL', 'admin@gmail.com') 
CLIENT_PASSWORD = os.getenv('CLIENT_PASSWORD', '123456')
BASE_URL = "http://localhost:8889/#/"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_experimental_option("detach", True)
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    # options.add_argument("--headless") # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

# --- HELPER FUNCTIONS ---


def handle_alert(driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        time.sleep(1) 
        return True, alert_text
    except TimeoutException:
        return False, None

def login_user(driver):
    """Đăng nhập nếu chưa đăng nhập"""
    if "/login" not in driver.current_url:
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'logout')]")))
            return
        except:
            driver.get(BASE_URL + "login")

    try:
        email_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(CLIENT_EMAIL)
        
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(CLIENT_PASSWORD)
        
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'] | //button[contains(text(), 'Đăng Nhập')] | //button[contains(text(), 'Đăng nhập')]")
        submit_btn.click()

        handle_alert(driver, timeout=5)
        WebDriverWait(driver, 10).until(EC.url_contains("/"))
    except Exception as e:
        print(f"Login check/action failed (might be already logged in): {e}")

def open_cart_page(driver):
    driver.get(BASE_URL + "cartshopping")
    WebDriverWait(driver, 10).until(EC.url_contains("cartshopping"))
    time.sleep(2) # Wait for cart to load as requested

def add_product_to_cart(driver, quantity=1):
    """Thêm sản phẩm đầu tiên vào giỏ"""
    print("[STEP] Bat dau them san pham vao gio...")
    driver.get(BASE_URL)
    try:
        
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/product/')]")))
        
        # Click first product
        products = driver.find_elements(By.XPATH, "//a[contains(@href, '/product/')]")
        if not products:
            print("   [ERROR] Khong tim thay san pham nao.")
            return False, "No products found on home page"
            
        first_product = products[0]
        driver.execute_script("arguments[0].scrollIntoView();", first_product)
        time.sleep(1)
        print("   -> Click vao san pham (JS)...")
        driver.execute_script("arguments[0].click();", first_product)
        
        WebDriverWait(driver, 15).until(EC.url_contains("/product/"))
        print("   -> Da chuyen sang trang chi tiet san pham.")
        
        # Click Add
        add_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Thêm vào giỏ hàng')]"))
        )
        
        time.sleep(0.5)
        
        # Retry click loop
        max_retries = 3
        for i in range(max_retries):
            print(f"   -> Click nut 'Them vao gio hang' (Attempt {i+1})...")
            
            add_btn.click()
            
            # Check for Confirm Alert
            print("   -> Dang cho alert xac nhan (Alert 1)...")
            is_confirm, confirm_text = handle_alert(driver, timeout=3)
            
            if is_confirm:
                print(f"   -> Alert 1: {is_confirm}, Noi dung: {confirm_text}")
                break
            else:
                print("   [WARN] Khong thay alert xac nhan. Thu click lai...")
                time.sleep(1)
        
        if not is_confirm:
             print("   [FAIL] Khong thay alert xac nhan sau cac lan thu.")
             
             return False, "No confirm alert"

        # Handle Success Alert
        print("   -> Dang xu ly alert thanh cong (Alert 2)...")
        is_success, success_text = handle_alert(driver, timeout=10)
        print(f"   -> Alert 2: {is_success}, Noi dung: {success_text}")
        
        if not is_success:
            print("   [WARN] Khong thay alert thanh cong. Kiem tra log browser...")
           
            
        return is_success, success_text
    except Exception as e:
        print(f"   [ERROR] Loi khi them san pham: {e}")
       
        return False, str(e)

def test_add_to_cart_success(driver):
    
    print("\n---: Add to Cart---")
    login_user(driver)
    
    is_alert, text = add_product_to_cart(driver)
    
    if is_alert and ("thành công" in text.lower() or "success" in text.lower()):
        print(f"[PASS] Alert success: {text}")
    else:
        # Fallback check: if item is in cart, maybe we missed the alert but it worked?
        open_cart_page(driver)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
            print("[PASS] Alert missed but item found in cart.")
        except:
            pytest.fail(f"[FAIL] Alert not success and item not found: {text}")

def test_view_cart_items(driver):
    """Xem danh sách sản phẩm trong giỏ"""
    print("\n--- View Cart Items ---")
    login_user(driver)
    open_cart_page(driver)
    
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        items = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        print(f"[PASS] Cart has {len(items)} items.")
    except TimeoutException:
        print("[INFO] Cart empty, trying to add item...")
        add_product_to_cart(driver)
        open_cart_page(driver)
        items = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        if len(items) > 0:
            print(f"[PASS] Cart has {len(items)} items (after retry).")
        else:
            pytest.fail("[FAIL] Cart is empty but should have items.")


def click_element_js(driver, element):
    """Helper: Click bằng Javascript để xử lý SVG hoặc phần tử bị che"""
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.5) # Chờ UI phản hồi nhẹ

def ensure_cart_has_item(driver):
    open_cart_page(driver)
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        print("   [INFO] Gio hang da co san pham.")
    except TimeoutException:
        print("   [INFO] Gio hang trong. Them san pham moi...")
        add_product_to_cart(driver)
        open_cart_page(driver)

def get_cart_item_quantity(driver, item_index=1):
    # Lấy text chứa số lượng. Cấu trúc React: <p> Số lượng: <svg> {qty} <svg> </p>
    xpath = f"(//div[contains(@class, 'font-bold')]//p)[{item_index}]"
    try:
        element = driver.find_element(By.XPATH, xpath)
        text = element.text # Selenium text thường bỏ qua SVG, chỉ lấy "Số lượng: 5"
        return int(''.join(filter(str.isdigit, text)))
    except:
        return 0

# --- CÁC TEST CASE ĐÃ SỬA ---

def test_update_quantity(driver):
    """Test chức năng tăng và giảm số lượng"""
    print("\n--- Test: Tang/Giam So Luong ---")
    login_user(driver)
    ensure_cart_has_item(driver)
    
    # XPath tìm SVG: SVG đầu là TRỪ, SVG sau là CỘNG trong cùng 1 thẻ <p>
    # Lưu ý: name()='svg' bắt buộc dùng cho thẻ svg trong XPath
    base_xpath = "(//div[contains(@class, 'font-bold')]//p)[1]"
    minus_btn_xpath = f"{base_xpath}/*[name()='svg'][1]"
    plus_btn_xpath = f"{base_xpath}/*[name()='svg'][2]"
    
    initial_qty = get_cart_item_quantity(driver)
    print(f" - So luong ban dau: {initial_qty}")
    
    # --- TEST TĂNG (+) ---
    print(" -> Click nut Tang (+) (JS Click)...")
    plus_btn = driver.find_element(By.XPATH, plus_btn_xpath)
    pus_btn.click()
    
    # Chờ số lượng thay đổi
    try:
        WebDriverWait(driver, 5).until(
            lambda d: get_cart_item_quantity(d) == initial_qty + 1
        )
        print(f" [PASS] So luong da tang len: {initial_qty + 1}")
    except TimeoutException:
        # Debug: In ra số lượng thực tế nếu fail
        actual = get_cart_item_quantity(driver)
        pytest.fail(f"[FAIL] So luong khong tang. Expect: {initial_qty + 1}, Actual: {actual}")

    # --- TEST GIẢM (-) ---
    print(" -> Click nut Giam (-) (JS Click)...")
    minus_btn = driver.find_element(By.XPATH, minus_btn_xpath)
    minus_btn.click()
    
    try:
        WebDriverWait(driver, 5).until(
            lambda d: get_cart_item_quantity(d) == initial_qty
        )
        print(f" [PASS] So luong da giam ve: {initial_qty}")
    except TimeoutException:
        actual = get_cart_item_quantity(driver)
        pytest.fail(f"[FAIL] So luong khong giam. Expect: {initial_qty}, Actual: {actual}")


def test_select_all_items(driver):
    """Test chức năng Chọn tất cả / Bỏ chọn tất cả"""
    print("\n--- Test: Chon Tat Ca / Bo Chon ---")
    login_user(driver)
    ensure_cart_has_item(driver)
    
    select_all_btn_xpath = "//button[contains(text(), 'Chọn tất cả') or contains(text(), 'Bỏ chọn tất cả')]"
    btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, select_all_btn_xpath)))
    
    # Đưa về trạng thái chưa chọn gì để bắt đầu test
    if "Bỏ chọn tất cả" in btn.text:
        print(" -> Reset trang thai: Bo chon tat ca truoc.")
        btn.click()
        time.sleep(1)
        btn = driver.find_element(By.XPATH, select_all_btn_xpath) # Lấy lại element

    # --- CASE 1: Click "Chọn tất cả" ---
    print(f" -> Click nut '{btn.text}'...")
    btn.click()
    
    # Wait logic: Chờ cho TẤT CẢ checkbox có trạng thái selected
    try:
        WebDriverWait(driver, 5).until(
            lambda d: all(cb.is_selected() for cb in d.find_elements(By.XPATH, "//input[@type='checkbox']"))
        )
        print(f" [PASS] Tat ca checkbox da duoc chon.")
    except TimeoutException:
        pytest.fail("[FAIL] Timeout: Mot so checkbox chua duoc chon sau khi an 'Chon tat ca'.")

    # --- CASE 2: Click "Bỏ chọn tất cả" ---
    # Lấy lại nút vì text đã đổi, DOM có thể đã đổi
    btn = driver.find_element(By.XPATH, select_all_btn_xpath)
    print(f" -> Click nut '{btn.text}' de huy chon...")
    btn.click()
    
    # Wait logic: Chờ cho KHÔNG CÒN checkbox nào selected
    try:
        WebDriverWait(driver, 5).until(
            lambda d: all(not cb.is_selected() for cb in d.find_elements(By.XPATH, "//input[@type='checkbox']"))
        )
        print(" [PASS] Da huy chon tat ca checkbox.")
    except TimeoutException:
        pytest.fail("[FAIL] Timeout: Van con checkbox duoc chon sau khi huy.")


def test_delete_item(driver):
    """Test chức năng Xóa sản phẩm"""
    print("\n--- Test: Xoa San Pham ---")
    login_user(driver)
    ensure_cart_has_item(driver)
    
    items_before = driver.find_elements(By.XPATH, "//div[contains(@class, 'bg-white shadow-sm')]")
    count_before = len(items_before)
    print(f" - So luong item truoc khi xoa: {count_before}")
    
    # Tìm nút xóa đầu tiên
    delete_btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "(//span[contains(text(), 'Xóa')])[1]"))
    )
    
    print(" -> Click nut Xoa (JS Click)...")
    # Dùng JS Click để đảm bảo event handler được kích hoạt
    delete_btn.click()
    
    # Xử lý Alert
    print(" -> Cho alert xac nhan xoa...")
    is_alert, text = handle_alert(driver, timeout=5)
    
    if is_alert:
        print(f" -> Da dong y alert: {text}")
        
        # Verify kết quả
        try:
            # Logic: Hoặc số lượng giảm đi 1, hoặc hiện thông báo giỏ hàng trống (nếu xóa item cuối)
            WebDriverWait(driver, 5).until(
                lambda d: len(d.find_elements(By.XPATH, "//div[contains(@class, 'bg-white shadow-sm')]")) == count_before - 1 
                or len(d.find_elements(By.XPATH, "//div[contains(text(), 'Bạn chưa có sản phẩm nào')]")) > 0
            )
            print(f" [PASS] Da xoa thanh cong.")
        except TimeoutException:
             pytest.fail(f"[FAIL] Item khong bien mat khoi DOM sau khi xoa.")
    else:
        pytest.fail("[FAIL] Khong thay alert xac nhan xoa xuat hien.")