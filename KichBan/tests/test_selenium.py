import time
from selenium.webdriver.common.by import By


def test_python_org_search(driver):
    """Mở python.org, tìm kiếm 'pytest' và kiểm tra kết quả."""
    driver.get("https://www.python.org")
    assert "Python" in driver.title

    search = driver.find_element(By.NAME, "q")
    search.clear()
    search.send_keys("pytest")
    search.submit()

    # đợi trang tải (dùng explicit wait là tốt hơn; dùng sleep cho ví dụ đơn giản)
    time.sleep(2)
    assert "pytest" in driver.page_source.lower()
