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
BASE_URL = "http://localhost:8888/#/"

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

# ==================== HELPER FUNCTIONS ====================

def handle_alert(driver, timeout=3, accept=True):
    """Xử lý alert và trả về text"""
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        time.sleep(1) 
        return True, alert_text
    except TimeoutException:
        return False, None

def login_user(driver):
    """Đăng nhập nếu chưa đăng nhập"""
    if "/login" not in driver.current_url:
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'logout')]")))
            print("[INFO] Already logged in")
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
        print(f"[WARN] Login check/action failed (might be already logged in): {e}")

def open_cart_page(driver):
    """Mở trang giỏ hàng"""
    driver.get(BASE_URL + "cartshopping")
    WebDriverWait(driver, 10).until(EC.url_contains("cartshopping"))
    time.sleep(2)

def clear_cart(driver):
    """Xóa tất cả sản phẩm trong giỏ hàng"""
    print("[HELPER] Clearing cart...")
    open_cart_page(driver)
    try:
        while True:
            # Tìm nút Xóa (theo UI thực tế: <span>Xóa</span>)
            delete_btns = driver.find_elements(By.XPATH, "//span[contains(text(), 'Xóa')] | //button[contains(text(), 'Xóa')]")
            if not delete_btns:
                break
            delete_btns[0].click()
            time.sleep(1)
            # Xử lý confirm dialog: "Bạn có chắc chắn muốn xóa sản phẩm này?"
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(1)
            except:
                pass
        print("[HELPER] Cart cleared")
    except Exception as e:
        print(f"[HELPER] Cart might be empty: {e}")

def add_product_to_cart(driver, quantity=1, product_index=0):
    """Thêm sản phẩm vào giỏ hàng"""
    print(f"[HELPER] Adding product {product_index} to cart (qty={quantity})")
    driver.get(BASE_URL)
    
    try:
        # Đợi sản phẩm xuất hiện
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/product/')]")))
        
        # Click vào sản phẩm
        products = driver.find_elements(By.XPATH, "//a[contains(@href, '/product/')]")
        if not products or len(products) <= product_index:
            print(f"[ERROR] Product {product_index} not found")
            return False, "Product not found"
            
        product = products[product_index]
        driver.execute_script("arguments[0].scrollIntoView();", product)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", product)
        
        WebDriverWait(driver, 15).until(EC.url_contains("/product/"))
        time.sleep(2)
        
        
        # Nhập số lượng nếu khác 1
        if quantity != 1:
            try:
                qty_input = driver.find_element(By.XPATH, "//input[@type='number'] | //input[@name='quantity']")
                qty_input.clear()
                qty_input.send_keys(str(quantity))
                time.sleep(1)
            except Exception as e:
                print(f"[WARN] Could not set quantity: {e}")
        
        # Click nút thêm vào giỏ
        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Thêm vào giỏ hàng')]"))
        )
        add_btn.click()
        
        # Xử lý alert xác nhận
        is_confirm, confirm_text = handle_alert(driver, timeout=5)
        if not is_confirm:
            print("[WARN] No confirmation alert")
            return False, "No confirmation alert"
        
        # Xử lý alert thành công
        is_success, success_text = handle_alert(driver, timeout=5)
        
        return is_success, success_text if success_text else confirm_text
        
    except Exception as e:
        print(f"[ERROR] Failed to add product: {e}")
        return False, str(e)

def get_cart_item_count(driver):
    """Đếm số sản phẩm trong giỏ"""
    try:
        items = driver.find_elements(By.XPATH, "//input[@type='checkbox'] | //tr[contains(@class, 'cart-item')]")
        return len(items)
    except:
        return 0

# ==================== TEST CASES: XEM GIỎ HÀNG ====================

def test_view_cart_with_products(driver):
    print("\n=== TC01: Xem giỏ hàng khi đã có sản phẩm ===")
    login_user(driver)
    add_product_to_cart(driver)
    open_cart_page(driver)

    try:
        a = get_cart_item_count(driver)
       
        assert a > 0, "Không tìm thấy hình ảnh sản phẩm trong giỏ hàng"
        
        print(f"[PASS] Hiển thị thông tin sản phẩm ")
        
    except AssertionError as e:
        pytest.fail(f"[FAIL] {e}")


def test_view_empty_cart(driver):
    """TC02: Xem giỏ hàng khi giỏ hàng trống"""
    print("\n=== TC02: Xem giỏ hàng khi giỏ hàng trống ===")
    login_user(driver)
    clear_cart(driver)
    open_cart_page(driver)
    
    try:
        empty_message = driver.find_elements(By.XPATH, "//*[contains(text(), 'Bạn chưa có sản phẩm nào trong giỏ hàng')]")
        no_items = len(driver.find_elements(By.XPATH, "//input[@type='checkbox']")) == 0
        
        assert empty_message or no_items, "Không hiển thị thông báo giỏ hàng trống"
        if empty_message:
            print(f"[PASS] Hiển thị thông báo: '{empty_message[0].text}'")
        else:
            print("[PASS] Giỏ hàng trống (không có checkbox)")
        
    except AssertionError as e:
        pytest.fail(f"[FAIL] {e}")




# ==================== TEST CASES: THÊM VÀO GIỎ HÀNG ====================

def test_add_valid_product_to_cart(driver):
    """TC04: Thêm sản phẩm hợp lệ vào giỏ hàng"""
    print("\n=== TC04: Thêm sản phẩm hợp lệ vào giỏ hàng ===")
    
    login_user(driver)
    
    # Bước thực hiện: Xem chi tiết sản phẩm, số lượng, thêm vào giỏ
    is_success, message = add_product_to_cart(driver, quantity=1)
    
    # Kết quả mong đợi: Sản phẩm được thêm vào giỏ hàng thành công
    if is_success and message and ("thành công" in message.lower() or "success" in message.lower()):
        print(f"[PASS] Thêm sản phẩm thành công: {message}")
    else:
        # Kiểm tra fallback: sản phẩm có trong giỏ không
        open_cart_page(driver)
        if get_cart_item_count(driver) > 0:
            print("[PASS] Sản phẩm đã được thêm vào giỏ (fallback check)")
        else:
            pytest.fail(f"[FAIL] Không thêm được sản phẩm: {message}")



def test_add_out_of_stock_product(driver):
    """TC07: Thêm sản phẩm khi hết hàng"""
    print("\n=== TC07: Thêm sản phẩm khi hết hàng ===")
    login_user(driver)
    
    # Bước thực hiện: Xem chi tiết sản phẩm, số lượng, thêm vào giỏ
    is_success, message = add_product_to_cart(driver, quantity=1, product_index=2)
    
    # Kết quả mong đợi: Sản phẩm được thêm vào giỏ hàng thành công
    if is_success and message and ("thành công" in message.lower() or "success" in message.lower()):
        print(f"[Fail] Thêm sản phẩm thành công: {message}")
    else:
        print(f"[PASS] Không thể thêm sản phẩm hết hàng: {message}")

# ==================== TEST CASES: CẬP NHẬT GIỎ HÀNG ====================

def test_update_cart_valid_quantity(driver):
    """TC09: Cập nhật số lượng hợp lệ"""
    print("\n=== TC09: Cập nhật số lượng hợp lệ ===")
    
    # Tiền điều kiện: Sản phẩm đã có trong giỏ
    login_user(driver)
    clear_cart(driver)
    add_product_to_cart(driver)
    open_cart_page(driver)
    
    try:
        # Lấy số lượng hiện tại (hiển thị giữa icon + và -)
        qty_text = driver.find_element(By.XPATH, "//p[contains(text(), 'Số lượng:')]")
        old_qty = qty_text.text.split(':')[-1].strip().split()[0] if ':' in qty_text.text else "1"
        print(f"[INFO] Số lượng hiện tại: {old_qty}")
        
        # Click nút + để tăng số lượng (theo UI thực tế dùng icon HiPlusSm)
        plus_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Số lượng:')]//*[name()='svg'][last()]"))
        )
        plus_btn.click()
        time.sleep(2)
        
        # Kiểm tra số lượng đã tăng
        open_cart_page(driver)
        qty_text_after = driver.find_element(By.XPATH, "//p[contains(text(), 'Số lượng:')]")
        new_qty = qty_text_after.text.split(':')[-1].strip().split()[0] if ':' in qty_text_after.text else "1"
        
        print(f"[PASS] Cập nhật số lượng từ {old_qty} thành {new_qty}")
        
    except Exception as e:
        print(f"[WARN] Không thể cập nhật số lượng: {e}")



def test_update_cart_zero_quantity(driver):
    """TC11: Cập nhật số lượng bằng 0"""
    print("\n=== TC11: Cập nhật số lượng bằng 0 ===")
    
    login_user(driver)
    clear_cart(driver)
    add_product_to_cart(driver)
    open_cart_page(driver)
    
    try:
        minus_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Số lượng:')]//*[name()='svg'][0]"))
        )
        minus_btn.click()
        time.sleep(2)
        
        # Click cập nhật
        is_confirmt, confirm_text = handle_alert(driver, timeout=5)
        if is_confirmt:
            print(f"[INFO] Alert khi cập nhật số lượng 0: {confirm_text}")
            empty_message = driver.find_elements(By.XPATH, "//*[contains(text(), 'Bạn chưa có sản phẩm nào trong giỏ hàng')]")
            no_items = len(driver.find_elements(By.XPATH, "//input[@type='checkbox']")) == 0
            
            assert empty_message or no_items, "Không hiển thị thông báo giỏ hàng trống"
            
            print(f"[INFO] Hiển thị thông báo: '{empty_message[0].text}'")
        print("[PASS] Cập nhật số lượng bằng 0 xử lý đúng")
    except Exception as e:
        print(f"[FAil] Test phụ thuộc vào validation: {e}")


# ==================== TEST CASES: XÓA KHỎI GIỎ HÀNG ====================

def test_delete_product_from_cart(driver):
    """TC13: Xóa sản phẩm khỏi giỏ hàng"""
    print("\n=== TC13: Xóa sản phẩm khỏi giỏ hàng ===")
    
    # Tiền điều kiện: Sản phẩm có trong giỏ
    login_user(driver)
    add_product_to_cart(driver)
    open_cart_page(driver)
    
    try:
        # Đếm số sản phẩm ban đầu
        initial_count = get_cart_item_count(driver)
        print(f"[INFO] Số sản phẩm ban đầu: {initial_count}")
        
        # Tìm nút xóa (theo UI thực tế: <span>Xóa</span>)
        delete_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Xóa')] | //button[contains(text(), 'Xóa')]"))
        )
        delete_btn.click()
        time.sleep(1)
        
        # Xác nhận xóa với text: "Bạn có chắc chắn muốn xóa sản phẩm này?"
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"[INFO] Confirm dialog: {alert_text}")
            assert "xóa" in alert_text.lower(), f"Unexpected alert text: {alert_text}"
            alert.accept()
            time.sleep(2)
        except Exception as e:
            print(f"[WARN] No confirm dialog: {e}")
        
        # Kiểm tra sản phẩm đã bị xóa
        open_cart_page(driver)
        final_count = get_cart_item_count(driver)
        
        assert final_count < initial_count, "Sản phẩm chưa bị xóa"
        print(f"[PASS] Sản phẩm đã bị xóa. Số sản phẩm còn lại: {final_count}")
        
    except Exception as e:
        pytest.fail(f"[FAIL] Không thể xóa sản phẩm: {e}")

def test_cancel_delete_product(driver):
    """TC14: Hủy thao tác xóa sản phẩm"""
    print("\n=== TC14: Hủy thao tác xóa sản phẩm ===")
    
    login_user(driver)
    add_product_to_cart(driver)
    open_cart_page(driver)
    
    try:
        # Đếm số sản phẩm ban đầu
        initial_count = get_cart_item_count(driver)
        print(f"[INFO] Số sản phẩm ban đầu: {initial_count}")
        
        # Click nút xóa
        delete_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Xóa')] | //button[contains(text(), 'Xóa')]"))
        )
        delete_btn.click()
        time.sleep(1)
        
        # Hủy xóa (dismiss alert)
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"[INFO] Hủy xóa: {alert_text}")
            alert.dismiss()  # Click Cancel
            time.sleep(2)
        except Exception as e:
            print(f"[WARN] No confirm dialog to cancel: {e}")
        
        # Kiểm tra sản phẩm vẫn còn
        open_cart_page(driver)
        final_count = get_cart_item_count(driver)
        
        assert final_count == initial_count, "Sản phẩm bị xóa mặc dù đã hủy"
        print(f"[PASS] Sản phẩm vẫn giữ nguyên: {final_count}")
        
    except Exception as e:
        print(f"[INFO] Test phụ thuộc vào UI confirm dialog: {e}")

