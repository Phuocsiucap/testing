from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ===== LambdaTest Credentials =====
LT_USERNAME = "nguyenvanphuoc09112004"
LT_ACCESS_KEY = "LT_2xdZAMQpu2eqeVw4d8neXuqRqTmuCe2fR5BTvPSMvhcsGQ2"

# ===== Handle Alert =====
def handle_alert(driver, timeout=3, accept=True):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        text = alert.text
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        return True, text
    except TimeoutException:
        return False, None


# ===== Login Test =====
def login_client(driver, browser_name):
    try:
        driver.get("https://testing-ao3c.onrender.com/#/login")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys("hung@gmail.com")

        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys("12345678")

        driver.find_element(By.XPATH, "//button[contains(text(), 'Đăng nhập')]").click()

        handle_alert(driver, timeout=5)

        WebDriverWait(driver, 10).until(EC.url_contains("/"))

        print(f"[PASS] Đăng nhập thành công trên {browser_name}")
        driver.execute_script("lambda-status=passed")

    except Exception as e:
        print(f"[FAIL] Đăng nhập thất bại trên {browser_name}: {str(e)}")
        driver.execute_script("lambda-status=failed")

    finally:
        driver.quit()


# ===== Create Driver =====
def create_driver(browser_name):
    if browser_name == "Chrome":
        options = ChromeOptions()
        options.set_capability("browserName", "Chrome")

    elif browser_name == "Edge":
        options = ChromeOptions()
        options.set_capability("browserName", "MicrosoftEdge")

    elif browser_name == "Firefox":
        options = FirefoxOptions()
        options.set_capability("browserName", "Firefox")

    else:
        raise ValueError("Browser không được hỗ trợ")

    options.set_capability("browserVersion", "latest")
    options.set_capability("platformName", "Windows 11")

    options.set_capability("LT:Options", {
        "user": LT_USERNAME,
        "accessKey": LT_ACCESS_KEY,
        "build": "Cross Browser Login Test",
        "name": f"Login Test - {browser_name}",
        "network": True,
        "video": True,
        "console": True
    })

    return webdriver.Remote(
        command_executor="https://hub.lambdatest.com/wd/hub",
        options=options
    )


# ===== Run Cross-Browser Test =====
if __name__ == "__main__":
    browsers = ["Chrome", "Edge", "Firefox"]

    for browser in browsers:
        print(f"\n=== Testing on {browser} ===")
        driver = create_driver(browser)
        login_client(driver, browser)
