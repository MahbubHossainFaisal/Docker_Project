# 🐳 Dockerized Flask & MySQL API

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

A containerized backend application built with **Flask (Python)** and **MySQL**, managed seamlessly through **Docker Compose**. This project serves as a robust foundation for receiving, storing, and tracking data metrics via a RESTful API.

---

## ✨ Features

- **RESTful API**: Easily ingest data and retrieve metrics via HTTP endpoints.
- **Containerized Database**: Persistent MySQL database configured with Docker volumes.
- **Health Checks**: Automated connectivity and service health monitoring configured in Compose.
- **Custom Networking**: Isolated Docker network for secure communication between containers.

---

## 📁 Project Structure

```text
📦 Docker_Project
 ┣ 📂 Flask_App           # Python API service
 ┃ ┣ 📜 app.py            # Main application logic and routing
 ┃ ┣ 📜 requirements.txt  # Python dependencies
 ┃ ┗ 📜 Dockerfile        # Flask image instructions
 ┣ 📂 MySQL               # Database service
 ┃ ┣ 📜 init-db.sql       # Initial schema & data (mounted on startup)
 ┃ ┗ 📜 Dockerfile        # MySQL image instructions
 ┣ 📜 compose.yaml        # Docker Compose configuration
 ┗ 📜 README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Run the Application (Recommended Method)

The easiest way to spin up both the database and the API is using Docker Compose.

1. **Start the containers** in the background:
   ```bash
   docker compose up -d --build
   ```

2. **Verify services are running** and healthy:
   ```bash
   docker compose ps
   ```

3. **Stop the application**:
   ```bash
   docker compose down
   ```

---

## 📡 API Endpoints

Once the application is running, the API is accessible at `http://127.0.0.1:8000`.

### 1. Check Health
Verify that the API is running and successfully connected to the database.
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy"
}
```

### 2. Ingest Data
Send user data to be stored in the MySQL database.
```http
POST /api/data
Content-Type: application/json

{
  "user_id": 2,
  "value": 29.5,
  "source": "api_test"
}
```

**Testing via PowerShell / cURL:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/data" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"user_id": 2, "value": 29.5}'
```
```bash
curl.exe -X POST http://127.0.0.1:8000/api/data -H "Content-Type: application/json" -d "{\"user_id\": 2, \"value\": 29.5}"
```

### 3. Get Metrics
Retrieve global ingestion statistics from the database.
```http
GET /api/metrics
```

---

## 🛠️ Manual Docker Commands (Reference)

If you prefer to run the containers manually without Compose (e.g., for troubleshooting), follow these steps:

**1. Create a custom network**
```bash
docker network create my_project_network
```

**2. Build the images**
```bash
docker build ./MySQL -t project_mysql_image
docker build ./Flask_App -t project_flask_image
```

**3. Run the MySQL container**
```bash
docker run -d -p 3306:3306 --name project_mysql_container --network my_project_network project_mysql_image
```

**4. Run the Flask container**
```bash
docker run -d -p 8000:8000 --name project_flask_container --network my_project_network project_flask_image
```

**5. Clean up manual containers**
```bash
docker rm -f project_mysql_container project_flask_container
```

---

## 🗄️ Interacting with the Database

You can execute queries directly against the MySQL container using Docker Compose. This is useful for manual verification:

```bash
# Insert dummy data manually
docker compose exec mysql mysql -u root -proot testdb -e "INSERT INTO ingested_data(user_id, value, source) VALUES (100, 2.32, 'dummy');"

# View all ingested data
docker compose exec mysql mysql -u root -proot testdb -e "SELECT * FROM ingested_data;"
```
