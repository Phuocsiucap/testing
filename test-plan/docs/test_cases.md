# PHDshop Test Cases Documentation

## Mục lục
1. [API Test Cases (Postman)](#1-api-test-cases-postman)
2. [UI Test Cases (Selenium)](#2-ui-test-cases-selenium)
3. [Performance Test Cases (JMeter)](#3-performance-test-cases-jmeter)

---

## 1. API Test Cases (Postman)

### 1.1 Authentication Module

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_API_AUTH_001 | Register User | Đăng ký user mới | None | 1. POST /api/user/register với valid data | Status 201, User created | High |
| TC_API_AUTH_002 | Register with existing email | Đăng ký với email đã tồn tại | Email đã tồn tại | 1. POST /api/user/register với email đã có | Status 400, Error message | High |
| TC_API_AUTH_003 | Login with valid credentials | Đăng nhập với thông tin hợp lệ | User đã tồn tại | 1. POST /api/user/login/ với valid credentials | Status 200, access_token, refresh_token | Critical |
| TC_API_AUTH_004 | Login with invalid password | Đăng nhập với password sai | User đã tồn tại | 1. POST /api/user/login/ với password sai | Status 401, Error message | High |
| TC_API_AUTH_005 | Get User Profile | Lấy thông tin user | User đã login | 1. GET /api/user/profile/ với token | Status 200, User info | High |
| TC_API_AUTH_006 | Get Profile without token | Lấy profile không có token | None | 1. GET /api/user/profile/ không có token | Status 401 | High |
| TC_API_AUTH_007 | Update User Profile | Cập nhật thông tin user | User đã login | 1. PATCH /api/user/update/ với data mới | Status 200, Updated info | Medium |

### 1.2 Products Module

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_API_PROD_001 | Get All Products | Lấy danh sách sản phẩm | Products exist | 1. GET /api/goods/list | Status 200, Array of products | Critical |
| TC_API_PROD_002 | Get Product by ID | Lấy sản phẩm theo ID | Product exists | 1. GET /api/goods/list/{id}/ | Status 200, Product details | High |
| TC_API_PROD_003 | Get Non-existent Product | Lấy sản phẩm không tồn tại | None | 1. GET /api/goods/list/99999/ | Status 404 | Medium |
| TC_API_PROD_004 | Get Products by Category | Lấy sản phẩm theo category | Category exists | 1. GET /api/goods/{category_id}/getByCategoryId | Status 200, Filtered products | High |
| TC_API_PROD_005 | Get Products by Brand | Lấy sản phẩm theo brand | Brand exists | 1. GET /api/goods/{brand_id}/getByBrandId | Status 200, Filtered products | High |

### 1.3 Cart Module

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_API_CART_001 | Get Cart | Lấy thông tin giỏ hàng | User logged in | 1. GET /api/cart/ với token | Status 200, Cart data | Critical |
| TC_API_CART_002 | Add Product to Cart | Thêm sản phẩm vào giỏ | User logged in, Product exists | 1. POST /api/cart/add/ với good_id, quantity | Status 200/201 | Critical |
| TC_API_CART_003 | Update Cart Item Quantity | Cập nhật số lượng | Item in cart | 1. PUT /api/cart/update/{cart_good_id}/ | Status 200 | High |
| TC_API_CART_004 | Remove Item from Cart | Xóa sản phẩm khỏi giỏ | Item in cart | 1. DELETE /api/cart/remove/{cart_good_id}/ | Status 200/204 | High |
| TC_API_CART_005 | Add Invalid Product | Thêm sản phẩm không tồn tại | User logged in | 1. POST /api/cart/add/ với invalid good_id | Status 400/404 | Medium |

### 1.4 Order Module

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_API_ORDER_001 | Create Order | Tạo đơn hàng mới | User logged in, Valid products | 1. POST /api/order/ với order data | Status 201, Order created | Critical |
| TC_API_ORDER_002 | Get Order List | Lấy danh sách đơn hàng | User has orders | 1. GET /api/order/order_list/ | Status 200, Array of orders | High |
| TC_API_ORDER_003 | Get Order Detail | Lấy chi tiết đơn hàng | Order exists | 1. GET /api/order/order_detail/{id}/ | Status 200, Order details | High |
| TC_API_ORDER_004 | Cancel Order | Hủy đơn hàng | Order exists, Cancellable | 1. POST /api/order/cancel_order/{id}/ | Status 200 | High |
| TC_API_ORDER_005 | Create Order with Empty Goods | Tạo đơn với goods rỗng | User logged in | 1. POST /api/order/ với empty goods | Status 400 | Medium |

### 1.5 Voucher Module

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_API_VOUCH_001 | Get All Vouchers | Lấy danh sách voucher | Vouchers exist | 1. GET /api/vouchers/ | Status 200, Array of vouchers | High |
| TC_API_VOUCH_002 | Redeem Voucher | Đổi voucher | User logged in, Voucher exists | 1. POST /api/vouchers/redeem/{id}/ | Status 200/201 | High |
| TC_API_VOUCH_003 | Get Redeemed Vouchers | Lấy voucher đã đổi | User has redeemed | 1. GET /api/vouchers/redeemed_vouchers/ | Status 200 | Medium |

### 1.6 Admin Module

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_API_ADMIN_001 | Admin Login | Đăng nhập admin | Admin account exists | 1. POST /api/admin/login/ | Status 200, Token | Critical |
| TC_API_ADMIN_002 | Get All Users | Lấy danh sách users | Admin logged in | 1. GET /api/admin/users/ | Status 200, Users array | High |
| TC_API_ADMIN_003 | Get Total Users | Lấy tổng số users | Admin logged in | 1. GET /api/admin/total-users/ | Status 200, Count | Medium |
| TC_API_ADMIN_004 | Get All Products (Admin) | Lấy danh sách products | Admin logged in | 1. GET /api/admin/goods/ | Status 200 | High |
| TC_API_ADMIN_005 | Create Product (Admin) | Tạo sản phẩm mới | Admin logged in | 1. POST /api/admin/goods/ | Status 201 | High |
| TC_API_ADMIN_006 | Get All Orders (Admin) | Lấy danh sách orders | Admin logged in | 1. GET /api/admin/orders/ | Status 200 | High |
| TC_API_ADMIN_007 | Get Monthly Revenue | Lấy doanh thu tháng | Admin logged in | 1. GET /api/admin/revenue/monthly/ | Status 200 | Medium |
| TC_API_ADMIN_008 | Get Today Revenue | Lấy doanh thu hôm nay | Admin logged in | 1. GET /api/admin/today-revenue/ | Status 200 | Medium |

---

## 2. UI Test Cases (Selenium)

### 2.1 Authentication UI

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_UI_AUTH_001 | Login Page Load | Kiểm tra trang login load | None | 1. Navigate to /login | Email, password fields, login button visible | Critical |
| TC_UI_AUTH_002 | Login Success | Đăng nhập thành công | Valid user | 1. Enter email 2. Enter password 3. Click login | Redirect to home, user logged in | Critical |
| TC_UI_AUTH_003 | Login Fail - Invalid | Đăng nhập thất bại | None | 1. Enter invalid credentials 2. Click login | Error message displayed | High |
| TC_UI_AUTH_004 | Login Fail - Empty Email | Email trống | None | 1. Leave email empty 2. Enter password 3. Click login | Validation error | High |
| TC_UI_AUTH_005 | Login Fail - Empty Password | Password trống | None | 1. Enter email 2. Leave password empty 3. Click login | Validation error | High |
| TC_UI_AUTH_006 | Register Page Load | Kiểm tra trang register | None | 1. Navigate to /regester | Form fields visible | High |
| TC_UI_AUTH_007 | Register Success | Đăng ký thành công | None | 1. Fill valid data 2. Submit | Success message or redirect | High |
| TC_UI_AUTH_008 | Navigate Login to Register | Điều hướng login -> register | None | 1. Go to login 2. Click register link | Navigate to register page | Medium |

### 2.2 Product Browsing UI

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_UI_PROD_001 | Home Page Products | Hiển thị sản phẩm trang chủ | Products exist | 1. Navigate to home | Products displayed | Critical |
| TC_UI_PROD_002 | Product Detail Page | Xem chi tiết sản phẩm | Product exists | 1. Click on product | Product detail page loads | Critical |
| TC_UI_PROD_003 | Product Has Title | Sản phẩm có tiêu đề | On product page | 1. Check title | Title is displayed | High |
| TC_UI_PROD_004 | Product Has Price | Sản phẩm có giá | On product page | 1. Check price | Price is displayed | High |
| TC_UI_PROD_005 | Add to Cart Button | Nút thêm giỏ hàng | On product page | 1. Check button | Button is visible | High |
| TC_UI_PROD_006 | Quantity Increase | Tăng số lượng | On product page | 1. Click increase button | Quantity increases | Medium |
| TC_UI_PROD_007 | Quantity Decrease | Giảm số lượng | On product page | 1. Click decrease button | Quantity decreases | Medium |
| TC_UI_PROD_008 | Navigate to Laptops | Điều hướng laptop | None | 1. Click laptop category | Navigate to laptop page | High |
| TC_UI_PROD_009 | Navigate to Mouse | Điều hướng mouse | None | 1. Click mouse category | Navigate to mouse page | High |
| TC_UI_PROD_010 | Navigate to Keyboard | Điều hướng keyboard | None | 1. Click keyboard category | Navigate to keyboard page | High |

### 2.3 Shopping Cart UI

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_UI_CART_001 | Cart Page Load | Trang giỏ hàng load | User logged in | 1. Navigate to /cartshopping | Cart page loads | Critical |
| TC_UI_CART_002 | Add Product to Cart | Thêm sản phẩm vào giỏ | User logged in | 1. Go to product 2. Click add to cart | Product added, success message | Critical |
| TC_UI_CART_003 | View Cart Items | Xem sản phẩm trong giỏ | Items in cart | 1. Go to cart | Items displayed | High |
| TC_UI_CART_004 | Update Item Quantity | Cập nhật số lượng | Item in cart | 1. Change quantity | Quantity updated | High |
| TC_UI_CART_005 | Remove Item | Xóa sản phẩm | Item in cart | 1. Click remove | Item removed | High |
| TC_UI_CART_006 | Empty Cart Message | Thông báo giỏ trống | Empty cart | 1. Go to empty cart | Empty message displayed | Medium |
| TC_UI_CART_007 | Checkout Button | Nút thanh toán | Items in cart | 1. Check checkout button | Button is visible | High |
| TC_UI_CART_008 | Cart Persists Refresh | Giỏ hàng lưu khi refresh | Items in cart | 1. Add items 2. Refresh page | Items still in cart | High |

### 2.4 Admin UI

| Test Case ID | Test Case Name | Description | Pre-conditions | Test Steps | Expected Result | Priority |
|--------------|----------------|-------------|----------------|------------|-----------------|----------|
| TC_UI_ADMIN_001 | Admin Login Page | Trang login admin | None | 1. Navigate to /admin/login | Login form displayed | Critical |
| TC_UI_ADMIN_002 | Admin Login Success | Đăng nhập admin | Valid admin | 1. Enter credentials 2. Submit | Navigate to dashboard | Critical |
| TC_UI_ADMIN_003 | Admin Login Fail | Đăng nhập thất bại | None | 1. Enter invalid credentials | Error message | High |
| TC_UI_ADMIN_004 | Dashboard Statistics | Hiển thị thống kê | Admin logged in | 1. Go to dashboard | Stats displayed | High |
| TC_UI_ADMIN_005 | Navigate to Users | Điều hướng quản lý user | Admin logged in | 1. Click users menu | Navigate to user management | High |
| TC_UI_ADMIN_006 | Navigate to Products | Điều hướng quản lý sản phẩm | Admin logged in | 1. Click products menu | Navigate to product management | High |
| TC_UI_ADMIN_007 | Navigate to Orders | Điều hướng quản lý đơn hàng | Admin logged in | 1. Click orders menu | Navigate to order management | High |
| TC_UI_ADMIN_008 | User List Display | Hiển thị danh sách user | In user management | 1. View user list | Users displayed | Medium |
| TC_UI_ADMIN_009 | Product List Display | Hiển thị danh sách sản phẩm | In product management | 1. View product list | Products displayed | Medium |

---

## 3. Performance Test Cases (JMeter)

### 3.1 Load Testing

| Test Case ID | Test Case Name | Description | Configuration | Acceptance Criteria | Priority |
|--------------|----------------|-------------|---------------|---------------------|----------|
| TC_PERF_001 | Authentication Load | Login với 50 concurrent users | 50 threads, 10 loops, 30s ramp-up | Response time < 3s, Error rate < 5% | Critical |
| TC_PERF_002 | Product List Load | Get products với 100 users | 100 threads, 20 loops, 60s ramp-up | Response time < 2s, Error rate < 5% | Critical |
| TC_PERF_003 | Product Detail Load | Get product detail với 100 users | 100 threads, 20 loops, 60s ramp-up | Response time < 2s, Error rate < 5% | High |
| TC_PERF_004 | Cart Operations Load | Cart operations với 30 users | 30 threads, 5 loops, 30s ramp-up | Response time < 3s, Error rate < 5% | High |
| TC_PERF_005 | Order Creation Load | Create orders với 20 users | 20 threads, 3 loops, 20s ramp-up | Response time < 5s, Error rate < 5% | High |

### 3.2 Stress Testing

| Test Case ID | Test Case Name | Description | Configuration | Acceptance Criteria | Priority |
|--------------|----------------|-------------|---------------|---------------------|----------|
| TC_STRESS_001 | High Load - Products | Get products với 200 users | 200 threads, 50 loops, 120s ramp-up, 5 min duration | System remains stable | High |
| TC_STRESS_002 | Spike Test | Sudden load increase | 0-500 threads trong 30s | System recovers | Medium |
| TC_STRESS_003 | Endurance Test | Extended load period | 50 threads, 4 hours duration | No memory leaks | Medium |

### 3.3 Performance Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Response Time (Average) | Thời gian phản hồi trung bình | < 2 seconds |
| Response Time (90th Percentile) | 90% requests nhanh hơn | < 3 seconds |
| Response Time (95th Percentile) | 95% requests nhanh hơn | < 5 seconds |
| Throughput | Số requests per second | > 100 RPS |
| Error Rate | Tỷ lệ lỗi | < 5% |
| Concurrent Users | Số users đồng thời | >= 100 |

---

## Test Execution Checklist

### Pre-Test Checklist
- [ ] Backend server running (http://localhost:8000)
- [ ] Frontend server running (http://localhost:5173)
- [ ] Database seeded with test data
- [ ] Test user accounts created
- [ ] Admin account created
- [ ] Products, categories, brands exist

### Post-Test Checklist
- [ ] Collect test results
- [ ] Generate reports
- [ ] Document bugs found
- [ ] Clean up test data if needed
- [ ] Archive test artifacts

---

## Defect Severity Levels

| Level | Description | Example |
|-------|-------------|---------|
| Critical | System crash, data loss, security breach | Login bypass, payment failure |
| High | Major feature not working | Cannot add to cart, cannot checkout |
| Medium | Feature works but has issues | Slow response, UI misalignment |
| Low | Minor issues, cosmetic | Typo, minor UI issue |

---

*Last Updated: 30/11/2025*
*Version: 1.0*
