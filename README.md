# 📊 Employee Statistics API

A FastAPI-based service to serve statistical insights (salary, experience, industry, gender distribution, and correlations) from a dataset of employee records.

---

## 🚀 Features
- Salary and experience statistics
- Age calculation and distribution
- Industry and gender demographics
- Correlation analysis
- Swagger UI and ReDoc documentation
- Dockerized with live reload and Nginx proxy

---

## 📁 Project Structure
```bash
.
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Settings/config
│   ├── services/        # Logic/processing
│   ├── data/            # JSON dataset
│   └── main.py          # FastAPI entry point
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
├── .dockerignore
├── .env (optional)
└── README.md
```

---

## ⚙️ Installation (Local)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Access:
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🐳 Dockerized Setup
### 1. Build and Run
```bash
docker-compose up --build
```

### 2. Access the App
- API Gateway: http://localhost
- Swagger UI: http://localhost/docs
- ReDoc UI: http://localhost/redoc

---

## 🔒 Environment Variables
You can define custom settings in `.env`:
```env
ENV=development
```

---

## 🔍 Debugging
### Check logs:
```bash
docker-compose logs api
```

### Restart everything:
```bash
docker-compose down
docker-compose up --build
```

---

## 📦 Dependencies
```
fastapi
uvicorn[standard]
pandas
pydantic
pydantic-settings
```

---
