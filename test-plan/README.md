# PHDshop Test Plan

## Tổng quan

Test Plan này được thiết kế để kiểm thử toàn diện hệ thống PHDshop - một ứng dụng e-commerce bao gồm:
- **Backend**: Django REST Framework API
- **Frontend**: React + Vite

## Công cụ kiểm thử

| Công cụ | Mục đích | Phiên bản đề xuất |
|---------|----------|-------------------|
| **Postman** | API Testing, Integration Testing | v10.x+ |
| **Selenium** | UI/E2E Testing, Browser Automation | v4.x+ |
| **JMeter** | Performance Testing, Load Testing | v5.6+ |

## Cấu trúc thư mục

```
test-plan/
├── README.md                    # Tài liệu này
├── postman/                     # Postman collections và environments
│   ├── PHDshop_API_Collection.json
│   └── PHDshop_Environment.json
├── selenium/                    # Selenium test scripts (Python)
│   ├── requirements.txt
│   ├── conftest.py
│   ├── pages/                   # Page Object Models
│   └── tests/                   # Test cases
├── jmeter/                      # JMeter test plans
│   └── PHDshop_LoadTest.jmx
└── docs/                        # Tài liệu bổ sung
    ├── test_cases.md
    ├── test_report_template.md
    └── setup_guide.md
```

## Phạm vi kiểm thử

### 1. API Testing (Postman)
- User Authentication (Register, Login)
- Product Management (CRUD)
- Cart Operations
- Order Management
- Voucher System
- Admin APIs

### 2. UI Testing (Selenium)
- User Registration & Login flows
- Product browsing & search
- Shopping cart operations
- Checkout process
- Admin dashboard

### 3. Performance Testing (JMeter)
- Load testing với concurrent users
- Stress testing
- API response time measurement
- Database connection pooling

## Cách sử dụng

### Setup môi trường
```bash
# Clone test-plan
cd test-plan

# Setup Selenium tests
cd selenium
pip install -r requirements.txt

# Import Postman collection
# File -> Import -> postman/PHDshop_API_Collection.json

# JMeter
# Mở JMeter và load file jmeter/PHDshop_LoadTest.jmx
```

### Chạy tests

```bash
# Postman CLI (Newman)
newman run postman/PHDshop_API_Collection.json -e postman/PHDshop_Environment.json

# Selenium
cd selenium
pytest tests/ -v --html=reports/report.html

# JMeter CLI
jmeter -n -t jmeter/PHDshop_LoadTest.jmx -l results.jtl -e -o reports/
```

## Môi trường kiểm thử

| Môi trường | Backend URL | Frontend URL |
|------------|-------------|--------------|
| Development | http://localhost:8000 | http://localhost:8888 |
| Staging | TBD | TBD |
| Production | TBD | TBD |

## Liên hệ

- Project: PHDshop
- Test Plan Version: 1.0
- Ngày tạo: 30/11/2025
