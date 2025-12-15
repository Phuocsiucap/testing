# PHDshop Test Environment Setup Guide

## Mục lục
1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Cài đặt Backend](#2-cài-đặt-backend)
3. [Cài đặt Frontend](#3-cài-đặt-frontend)
4. [Cài đặt Postman](#4-cài-đặt-postman)
5. [Cài đặt Selenium](#5-cài-đặt-selenium)
6. [Cài đặt JMeter](#6-cài-đặt-jmeter)
7. [Chạy Tests](#7-chạy-tests)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Yêu cầu hệ thống

### Hardware
- CPU: 4 cores trở lên
- RAM: 8GB trở lên (16GB recommended cho JMeter)
- Storage: 10GB free space

### Software
| Software | Phiên bản | Mục đích |
|----------|-----------|----------|
| Python | 3.9+ | Selenium tests, Django backend |
| Node.js | 18+ | Frontend |
| Java JDK | 11+ | JMeter |
| Chrome/Firefox/Edge | Latest | Selenium browser automation |
| Git | Latest | Version control |

---

## 2. Cài đặt Backend

### 2.1 Clone và Setup
```bash
cd d:\testing\backend\PHDshop

# Tạo virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2.2 Database Setup
```bash
# Chạy migrations
python manage.py migrate

# Tạo superuser (admin)
python manage.py createsuperuser
```

### 2.3 Seed Test Data
```bash
# Tạo test data (nếu có script)
python manage.py loaddata fixtures/test_data.json

# Hoặc tạo manual qua Django admin
python manage.py runserver
# Truy cập http://localhost:8000/admin/
```

### 2.4 Chạy Backend Server
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 3. Cài đặt Frontend

### 3.1 Install Dependencies
```bash
cd d:\testing\frontend

# Cài đặt packages
npm install
```

### 3.2 Chạy Development Server
```bash
npm run dev

# Server sẽ chạy tại http://localhost:5173
```

---

## 4. Cài đặt Postman

### 4.1 Download và Install
1. Download Postman từ: https://www.postman.com/downloads/
2. Cài đặt và đăng nhập (tùy chọn)

### 4.2 Import Collection
1. Mở Postman
2. Click **Import** (góc trên bên trái)
3. Chọn file: `test-plan/postman/PHDshop_API_Collection.json`
4. Click **Import**

### 4.3 Import Environment
1. Click **Import**
2. Chọn file: `test-plan/postman/PHDshop_Environment.json`
3. Click **Import**
4. Chọn environment "PHDshop Environment" từ dropdown

### 4.4 Cấu hình Environment Variables
1. Click vào icon "Environment" (góc phải)
2. Cập nhật các giá trị:
   - `base_url`: http://localhost:8000
   - `test_email`: email của test user
   - `test_password`: password của test user
   - `admin_email`: email của admin
   - `admin_password`: password của admin

### 4.5 Cài đặt Newman (CLI Runner)
```bash
# Cài đặt global
npm install -g newman

# Cài đặt HTML reporter
npm install -g newman-reporter-html
```

---

## 5. Cài đặt Selenium

### 5.1 Setup Python Environment
```bash
cd d:\testing\test-plan\selenium

# Tạo virtual environment (optional, có thể dùng chung với backend)
python -m venv venv
venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 5.2 WebDriver Setup
WebDriver sẽ được tự động download bởi `webdriver-manager`. Không cần cài đặt thủ công.

### 5.3 Tạo file .env
```bash
# Tạo file .env trong thư mục selenium
```

Nội dung file `.env`:
```env
BASE_URL=http://localhost:5173
API_URL=http://localhost:8000
BROWSER=chrome
HEADLESS=false
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
TEST_EMAIL=testuser@example.com
TEST_PASSWORD=Test@123456
ADMIN_EMAIL=admin@phdshop.com
ADMIN_PASSWORD=Admin@123456
```

### 5.4 Tạo thư mục reports
```bash
mkdir reports
mkdir reports\screenshots
```

---

## 6. Cài đặt JMeter

### 6.1 Download JMeter
1. Download từ: https://jmeter.apache.org/download_jmeter.cgi
2. Chọn phiên bản Binary (apache-jmeter-5.6.x.zip)
3. Giải nén vào thư mục (ví dụ: `C:\JMeter`)

### 6.2 Cấu hình Environment Variable
```bash
# Windows
setx JMETER_HOME "C:\JMeter\apache-jmeter-5.6"
setx PATH "%PATH%;%JMETER_HOME%\bin"
```

### 6.3 Cài đặt Plugins (Optional)
1. Download JMeter Plugins Manager: https://jmeter-plugins.org/install/Install/
2. Copy `jmeter-plugins-manager-x.x.jar` vào `%JMETER_HOME%\lib\ext`
3. Khởi động lại JMeter
4. Vào Options > Plugins Manager để cài thêm plugins

### 6.4 Mở Test Plan
```bash
# GUI Mode
jmeter -t "d:\testing\test-plan\jmeter\PHDshop_LoadTest.jmx"

# Hoặc double-click vào file .jmx
```

### 6.5 Cấu hình Test Plan
1. Mở file `PHDshop_LoadTest.jmx` trong JMeter
2. Cập nhật User Defined Variables:
   - `BASE_URL`: localhost
   - `PORT`: 8000
   - `PROTOCOL`: http

---

## 7. Chạy Tests

### 7.1 Chạy Postman Tests

#### GUI Mode
1. Mở Postman
2. Chọn Collection "PHDshop API Collection"
3. Click "Run Collection"
4. Chọn các test cases cần chạy
5. Click "Run PHDshop API Collection"

#### CLI Mode (Newman)
```bash
cd d:\testing\test-plan

# Chạy tất cả tests
newman run postman/PHDshop_API_Collection.json -e postman/PHDshop_Environment.json

# Chạy với HTML report
newman run postman/PHDshop_API_Collection.json -e postman/PHDshop_Environment.json -r html --reporter-html-export reports/postman_report.html

# Chạy folder cụ thể
newman run postman/PHDshop_API_Collection.json -e postman/PHDshop_Environment.json --folder "1. Authentication"
```

### 7.2 Chạy Selenium Tests

```bash
cd d:\testing\test-plan\selenium

# Chạy tất cả tests
pytest tests/ -v

# Chạy với HTML report
pytest tests/ -v --html=reports/report.html

# Chạy file cụ thể
pytest tests/test_authentication.py -v

# Chạy test class cụ thể
pytest tests/test_authentication.py::TestUserLogin -v

# Chạy test case cụ thể
pytest tests/test_authentication.py::TestUserLogin::test_login_with_valid_credentials -v

# Chạy với browser khác
pytest tests/ -v --browser=firefox

# Chạy headless mode
pytest tests/ -v --headless

# Chạy parallel (cần pytest-xdist)
pytest tests/ -v -n 4
```

### 7.3 Chạy JMeter Tests

#### GUI Mode
1. Mở JMeter
2. File > Open > `PHDshop_LoadTest.jmx`
3. Click nút Start (màu xanh)
4. Xem kết quả trong các Listeners

#### CLI Mode (Recommended for Load Testing)
```bash
cd d:\testing\test-plan\jmeter

# Chạy test và xuất kết quả
jmeter -n -t PHDshop_LoadTest.jmx -l results.jtl

# Chạy với HTML report
jmeter -n -t PHDshop_LoadTest.jmx -l results.jtl -e -o reports/

# Chạy với custom properties
jmeter -n -t PHDshop_LoadTest.jmx -l results.jtl -JBASE_URL=192.168.1.100 -JPORT=8000

# Chỉ chạy Thread Group cụ thể (enable/disable trong JMX)
```

---

## 8. Troubleshooting

### 8.1 Backend Issues

#### Port Already in Use
```bash
# Tìm process đang dùng port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

#### Database Errors
```bash
# Reset database
python manage.py flush
python manage.py migrate
```

### 8.2 Frontend Issues

#### Port Already in Use
```bash
# Đổi port trong vite.config.js hoặc dùng
npm run dev -- --port 3000
```

#### Module Not Found
```bash
# Xóa node_modules và reinstall
rm -rf node_modules
npm install
```

### 8.3 Selenium Issues

#### WebDriver Error
```bash
# Cập nhật webdriver-manager
pip install --upgrade webdriver-manager
```

#### Element Not Found
- Kiểm tra locator selector
- Tăng implicit/explicit wait
- Kiểm tra page đã load hoàn toàn

#### ChromeDriver Version Mismatch
```bash
# webdriver-manager sẽ tự động download đúng version
# Nếu vẫn lỗi, update Chrome browser lên version mới nhất
```

### 8.4 JMeter Issues

#### Out of Memory
```bash
# Sửa file jmeter.bat, tăng heap size
set HEAP=-Xms2g -Xmx4g
```

#### Connection Timeout
- Kiểm tra server đang chạy
- Kiểm tra firewall
- Tăng timeout trong HTTP Request Defaults

### 8.5 Postman/Newman Issues

#### SSL Certificate Error
```bash
# Tắt SSL verification
newman run collection.json --insecure
```

#### Environment Variables Not Working
- Kiểm tra environment đã được chọn
- Kiểm tra variable names chính xác

---

## Quick Reference Commands

```bash
# Start Backend
cd d:\testing\backend\PHDshop
python manage.py runserver

# Start Frontend
cd d:\testing\frontend
npm run dev

# Run Postman Tests
cd d:\testing\test-plan
newman run postman/PHDshop_API_Collection.json -e postman/PHDshop_Environment.json

# Run Selenium Tests
cd d:\testing\test-plan\selenium
pytest tests/ -v --html=reports/report.html

# Run JMeter Tests
cd d:\testing\test-plan\jmeter
jmeter -n -t PHDshop_LoadTest.jmx -l results.jtl -e -o reports/
```

---

*Last Updated: 30/11/2025*
