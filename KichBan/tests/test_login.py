import time
from selenium.webdriver.common.by import By


def test_login_success(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()
    time.sleep(1)
    flash = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in flash


def test_login_failure(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()
    time.sleep(1)
    flash = driver.find_element(By.ID, "flash").text
    assert ("Your username is invalid!" in flash) or ("Your password is invalid!" in flash)
