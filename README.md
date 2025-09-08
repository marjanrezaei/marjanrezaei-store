🛍️ Marjan Store – E-commerce API with Django REST Framework

**Live API:** [https://marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com)

Marjan Store is a fully-featured e-commerce backend built with Django and Django REST Framework.  
It supports user authentication, product browsing, cart management, and order processing.  
Interactive API documentation is available via Swagger and ReDoc.

---

## 🚀 Features

- 🔐 JWT-based user authentication (register/login)
- 🛒 Product listing and detail views
- 🛍️ Cart management per user
- 📦 Order creation and order history
- 🧑‍💼 Admin panel for product and order management
- 📚 Auto-generated API documentation (Swagger & ReDoc)

---

## 🧰 Tech Stack

- **Backend:** Django, Django REST Framework  
- **Authentication:** JWT via `djangorestframework-simplejwt`  
- **Documentation:** Swagger UI & ReDoc via `drf-yasg`  
- **Database:** PostgreSQL (or SQLite for local development)  
- **Deployment:** Render  
- **Local Dev:** Docker & Docker Compose

---

## 📚 API Documentation

Explore and test the API directly from your browser:

| Tool           | URL                                                                 |
|----------------|----------------------------------------------------------------------|
| **Swagger UI** | [`/swagger/`](https://marjanrezaei-store.onrender.com/swagger/)     |
| **Swagger JSON** | [`/swagger.json`](https://marjanrezaei-store.onrender.com/swagger.json) |
| **ReDoc**      | [`/redoc/`](https://marjanrezaei-store.onrender.com/redoc/)         |

---

## 🛠️ Manual Installation (Without Docker)

### 1. Clone the repository
```bash
git clone https://github.com/marjanrezaei/marjanrezaei-store.git
cd marjanrezaei-store
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Start the development server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 🐳 Local Development with Docker

For local development, use the Docker Compose file located in the `devops/` directory.

### Included Services

| Service       | Description                          | Port(s)     |
|---------------|--------------------------------------|-------------|
| `db`          | PostgreSQL 15 with persistent volume | 5432        |
| `redis`       | Redis for caching and Celery broker  | 6379        |
| `backend`     | Django development server            | 8000        |
| `worker`      | Celery worker                        | —           |
| `celery_beat` | Celery beat scheduler                | —           |
| `mailhog`     | Local SMTP testing tool              | 8025 (UI), 1025 (SMTP) |

### Run Locally with Docker

```bash
docker-compose -f devops/docker-compose.yml up --build
```

To stop the containers:

```bash
docker-compose -f devops/docker-compose.yml down
```

---

## 🔐 Authentication Flow

- **Register:** `POST /api/auth/register/`  
- **Login:** `POST /api/auth/login/`  
- Use the returned JWT token in the `Authorization` header:

```http
Authorization: Bearer <your_token>
```

---

## 📡 API Endpoints Overview

| Endpoint                  | Method     | Description             |
|---------------------------|------------|-------------------------|
| `/api/products/`          | GET        | List all products       |
| `/api/products/<id>/`     | GET        | Retrieve product details|
| `/api/cart/`              | GET/POST   | View or add to cart     |
| `/api/orders/`            | GET/POST   | View or create orders   |
| `/api/auth/register/`     | POST       | Register a new user     |
| `/api/auth/login/`        | POST       | Login and receive token |

---

## 🧪 Running Tests

To run tests manually:

```bash
python manage.py test
```

Or inside Docker:

```bash
docker exec backend python manage.py test
```

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.

---

## 👩‍💻 Author

**Marjan Rezaei**  
GitHub: [@marjanrezaei](https://github.com/marjanrezaei)  
Live API: [marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com)
