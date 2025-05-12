# Feedback Report Generator

A modular, containerized Django web service that asynchronously processes student event data to generate HTML and PDF feedback reports. This service uses Celery with Redis as a broker, PostgreSQL as the storage backend, and Flower for task monitoring.

---

## 🚀 Features

* Accepts JSON payloads with student event data
* Asynchronously generates:

  * HTML feedback reports (stored in PostgreSQL)
  * PDF reports (stored as binary in PostgreSQL)
* Task queueing and monitoring via Celery and Redis
* Flower dashboard for task tracking
* Fully Dockerized for reproducible deployment

---

## 📁 Project Structure

```
feedback-report-generator/
├── assignment/                # Django app with views, tasks, models
├── feedback_report/          # Django project configuration
├── templates/                # Optional HTML templates
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── entrypoint.sh             # Container entrypoint script
└── README.md
```

---

## ⚙️ Setup Instructions

### 📦 Prerequisites

* Docker Desktop (for Linux/Windows/Mac)

### 🚧 Run the Project

1. **Build and Start All Containers:**

   ```bash
   docker-compose build
      ```
    ```bash
   docker-compose up -d
      ```

2. **Access the App:**

   * API: [http://localhost:8000](http://localhost:8000)
   * Flower: [http://localhost:5555](http://localhost:5555)

---

## 🔹 API Endpoints

### 📂 `POST /assignment/html`

* **Input:** JSON payload with student event data
* **Output:** `{"task_id": "<celery_task_id>"}`
* **Description:** Enqueues a Celery task to generate an HTML report

### 🔹 `GET /assignment/html/<task_id>`

* **Output:** Status of task and HTML content if completed

---

### 📂 `POST /assignment/pdf`

* **Input:** Same as HTML endpoint
* **Output:** `{"task_id": "<celery_task_id>"}`
* **Description:** Enqueues a task to generate a PDF report

### 🔹 `GET /assignment/pdf/<task_id>`

* **Output:** Status of task or raw PDF as downloadable file

---


## 📊 Assumptions & Design Choices

* Each request handles one student record (first object in list)
* Unit IDs are converted to `Q1`, `Q2`, etc. based on sorted order
* Report content is stored directly in the database
* Redis is used only for message brokering (not data storage)
* Flower is used for local task monitoring only

---

## 📚 Tech Stack

* Django + DRF
* Celery + Redis
* PostgreSQL
* ReportLab (PDF generation)
* Flower (task monitoring)
* Docker + Docker Compose

---

## 🔧 Dev Tips

* View logs: `docker compose logs -f`
* Debug in shell:

  ```bash
  docker compose exec app python manage.py shell
  ```
* Stop services:

  ```bash
  docker compose down
  ```

---

## 📋 License

MIT © Aryan Bhardwaj
