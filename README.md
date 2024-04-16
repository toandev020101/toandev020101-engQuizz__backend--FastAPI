# EngQuizz: Thi Tiếng Anh Trực Tuyến

## Mô Tả

Dự án này là một ứng dụng backend được xây dựng bằng FastAPI, sử dụng Poetry để quản lý dependencies và Alembic để quản lý cơ sở dữ liệu. Dự án cung cấp các API để xử lý các yêu cầu từ phía frontend hoặc các ứng dụng khác thông qua HTTP.

## Cài Đặt

1. Clone repository:

   ```bash
   git clone https://github.com/toandev020101/toandev020101-engQuizz__backend--FastAPI.git
   cd toandev020101-toandev020101-engQuizz__backend--FastAPI
   ```

2. Cài đặt Poetry (nếu chưa có):

   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
   ```

   hoặc

   ```bash
   pip install poetry
   ```

3. Cài đặt venv:
   Window

   ```bash
   python -m venv venv
   cd venv/Scripts
   activate
   cd ../../
   ```

   Linux

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Cài đặt dependencies:

   ```bash
   poetry install
   ```

5. Cấu hình file .env

6. Tạo cơ sở dữ liệu:

   ```bash
   alembic upgrade head
   ```

## Sử Dụng

Để chạy ứng dụng, bạn có thể sử dụng Poetry để chạy lệnh FastAPI:

```bash
poetry run uvicorn app.main:app --reload
```

hoặc

```bash
poetry run start
```
