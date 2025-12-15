# Selenium test sample (Python)

Hướng dẫn nhanh để chạy test Selenium đơn giản bằng Python + pytest.

Yêu cầu:
- Python (3.8+)
- Google Chrome được cài trên máy (driver sẽ được quản lý tự động bởi `webdriver-manager`).

Cài dependencies và chạy test (PowerShell):

```powershell
python -m pip install -r requirements.txt
pytest
```

Gợi ý:
- Để xem trình duyệt khi chạy, mở file `g:/KichBan/tests/test_selenium.py` và xóa hoặc comment dòng `opts.add_argument("--headless=new")`.
- Nếu muốn chạy với Firefox, sửa fixture `driver()` để sử dụng `webdriver_manager.firefox` và `webdriver.Firefox()`.
