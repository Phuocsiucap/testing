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

# Load environment variables
load_dotenv()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin@gmail.com') 
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '123456')
BASE_URL = "https://testing-ao3c.onrender.com/#/"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_experimental_option("detach", True)
    # options.add_argument("--headless") # Bỏ comment nếu muốn chạy không giao diện
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def handle_alert(driver, timeout=3):
    """Hàm xử lý đóng alert thông báo (nếu có)"""
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        time.sleep(0.5) # Chờ alert đóng hẳn
        return True, alert_text
    except TimeoutException:
        return False, None

def login_admin(driver):
    """Đăng nhập và xử lý alert thành công"""
    if "admin/login" not in driver.current_url:
        driver.get(BASE_URL + "admin/login")

    # Check nhanh nếu đã ở trong trang admin rồi
    try:
        WebDriverWait(driver, 2).until(EC.url_contains("admin/manageuser"))
        return
    except:
        pass

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(ADMIN_USERNAME)
    
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
    
    driver.find_element(By.XPATH, "//button[text()='Đăng Nhập']").click()

    # Xử lý Alert "Đăng nhập thành công"
    is_alert, text = handle_alert(driver, timeout=10)
    if is_alert:
        print(f"\n   ℹ️  Info: Đã đóng alert '{text}'")

    WebDriverWait(driver, 10).until(EC.url_contains("admin"))

def get_row_count(driver):
    return len(driver.find_elements(By.XPATH, "//table/tbody/tr"))

# ================= TEST CASES =================

def test_hien_thi_danh_sach_nguoi_dung(driver):
    print("\n---------------------------------------------------")
    print("▶️  Bắt đầu test: Hiển thị danh sách người dùng")
    login_admin(driver)
    driver.get(BASE_URL + "admin/manageuser")
    
    handle_alert(driver) # Clear alert tồn đọng

    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    assert table.is_displayed()
    
    headers = driver.find_elements(By.XPATH, "//table/thead/tr/th")
    actual_headers = [h.text.upper() for h in headers]
    expected_headers = ["TÊN NGƯỜI DÙNG", "EMAIL", "THAO TÁC"]
    
    assert actual_headers == expected_headers
    
    # --- THÔNG BÁO SUCCESS ---
    print("✅ [PASS] Bảng người dùng hiển thị đúng header và dữ liệu.")

def test_xem_thong_tin_chi_tiet_tai_khoan(driver):
    print("\n---------------------------------------------------")
    print("▶️  Bắt đầu test: Xem chi tiết tài khoản")
    login_admin(driver)
    driver.get(BASE_URL + "admin/manageuser")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))

    # Click nút xem (Con mắt)
    driver.find_element(By.XPATH, "//table/tbody/tr[1]//button[contains(@class, 'text-blue-600')]").click()

    # Chờ Modal
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Thông tin chi tiết')]"))
    )

    assert driver.find_element(By.XPATH, "//p[strong[contains(text(), 'Email')]]").is_displayed()
    
    # Đóng modal
    driver.find_element(By.XPATH, "//button[text()='Đóng']").click()
    
    # --- THÔNG BÁO SUCCESS ---
    print("✅ [PASS] Popup chi tiết hiển thị đầy đủ thông tin.")

def test_xoa_tai_khoan(driver):
    print("\n---------------------------------------------------")
    print("▶️  Bắt đầu test: Xóa tài khoản")
    login_admin(driver)
    driver.get(BASE_URL + "admin/manageuser")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))
    
    rows_before = get_row_count(driver)
    print(f"   ℹ️  Số dòng trước khi xóa: {rows_before}")

    # Click xóa
    driver.find_element(By.XPATH, "//table/tbody/tr[1]//button[contains(@class, 'text-red-600')]").click()

    # Alert 1: Confirm
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    print("   ℹ️  Đã chấp nhận alert xác nhận xóa.")

    # Alert 2: Success (QUAN TRỌNG)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert_success = driver.switch_to.alert
    print(f"   ℹ️  Thông báo từ hệ thống: {alert_success.text}")
    alert_success.accept()

    # Chờ số lượng dòng giảm đi 1
    WebDriverWait(driver, 10).until(lambda d: get_row_count(d) == rows_before - 1)
    
    rows_after = get_row_count(driver)
    assert rows_after == rows_before - 1

    # --- THÔNG BÁO SUCCESS ---
    print(f"✅ [PASS] Xóa thành công. Số dòng giảm từ {rows_before} xuống {rows_after}.")

def test_huy_thao_tac_xoa(driver):
    print("\n---------------------------------------------------")
    print("▶️  Bắt đầu test: Hủy thao tác xóa")
    login_admin(driver)
    driver.get(BASE_URL + "admin/manageuser")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))
    rows_before = get_row_count(driver)

    driver.find_element(By.XPATH, "//table/tbody/tr[1]//button[contains(@class, 'text-red-600')]").click()

    # Alert Confirm -> Dismiss
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.dismiss()
    print("   ℹ️  Đã chọn Cancel trên alert.")

    time.sleep(1) # Chờ UI ổn định
    rows_after = get_row_count(driver)
    
    assert rows_after == rows_before

    # --- THÔNG BÁO SUCCESS ---
    print(f"✅ [PASS] Hủy xóa thành công. Số dòng vẫn giữ nguyên là {rows_after}.")

