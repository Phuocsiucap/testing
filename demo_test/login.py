from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
LT_USERNAME = "nguyenvanphuoc09112004"
LT_ACCESS_KEY = "LT_2xdZAMQpu2eqeVw4d8neXuqRqTmuCe2fR5BTvPSMvhcsGQ2"

options = Options()

# Capabilities mới cho Selenium 4
options.set_capability("browserName", "Chrome")
options.set_capability("browserVersion", "latest")
options.set_capability("platformName", "Windows 11")

options.set_capability("LT:Options", {
    "user": LT_USERNAME,
    "accessKey": LT_ACCESS_KEY,
    "build": "Admin Web Test",
    "name": "Open Admin Page",
    "network": True,
    "video": True,
    "console": True
})

driver = webdriver.Remote(
    command_executor="https://hub.lambdatest.com/wd/hub",
    options=options
)

try:
    driver.get("https://testing-ao3c.onrender.com/#/admin")
    time.sleep(5)

    print("Title:", driver.title)

    driver.execute_script("lambda-status=passed")
finally:
    driver.quit()