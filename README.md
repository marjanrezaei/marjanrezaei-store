🛍️ Marjan Store – Multilingual E-commerce API

**Live Demo:** [https://marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com)  
**Author:** [@marjanrezaei](https://github.com/marjanrezaei)

Marjan Store is a scalable, multilingual e-commerce backend built with Django and Django REST Framework. It supports user authentication, product browsing, cart management, and order processing. The API is documented with Swagger and ReDoc, and supports Persian, English, and Arabic languages.

---

## 🚀 Features

- 🔐 JWT-based user authentication (register/login)
- 🛒 Product listing and detail views
- 🛍️ Cart management per user
- 📦 Order creation and order history
- 🧑‍💼 Admin panel for product and order management
- 🌐 Multilingual support (fa, en, ar)
- 📚 Auto-generated API documentation (Swagger & ReDoc)
- 🧭 Visual database diagram for model relationships

---

## 🧭 Database Diagram

The following diagram illustrates the relationships between core models such as `User`, `Product`, `Cart`, and `Order`.

![Database Diagram](https://raw.githubusercontent.com/marjanrezaei/marjanrezaei-store/main/docs/dbDiagram.png)

You can also [view the editable diagram](https://github.com/marjanrezaei/marjanrezaei-store/blob/main/docs/dbDiagram.drawio) using draw.io.

---

## 🧰 Tech Stack

| Layer            | Technology                              |
|------------------|------------------------------------------|
| Backend          | Django, Django REST Framework            |
| Auth             | JWT via `djangorestframework-simplejwt` |
| Docs             | Swagger UI & ReDoc via `drf-yasg`        |
| Database         | PostgreSQL (or SQLite for local dev)     |
| Task Queue       | Celery + Redis                           |
| Deployment       | Render                                   |
| Local Dev        | Docker & Docker Compose                  |
| i18n             | Django gettext + django-parler           |

---

## 🌍 Multilingual Support

Supports Persian (`fa`), English (`en`), and Arabic (`ar`) using Django’s internationalization framework and `django-parler`.

```python
LANGUAGES = [
    ('fa', _('فارسی')),
    ('en', _('English')),
    ('ar', _('العربية')),
]
```

Use `/set-language/` endpoint to switch interface language dynamically.

---

## 📚 API Documentation

Explore and test the API directly from your browser:

- [Swagger UI](https://marjanrezaei-store.onrender.com/swagger/)
- [Swagger JSON](https://marjanrezaei-store.onrender.com/swagger.json)
- [ReDoc](https://marjanrezaei-store.onrender.com/redoc/)

---

## 🛠️ Manual Installation

```bash
# Clone the repository
git clone https://github.com/marjanrezaei/marjanrezaei-store.git
cd marjanrezaei-store

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 🐳 Docker Setup

Use the Docker Compose file located in the `devops/` directory:

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

Use the returned JWT token in the `Authorization` header:

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
| `/set-language/`          | POST       | Switch interface language|

---
## 🗺️ Sitemap Integration

This project includes a dynamic, multilingual sitemap powered by Django’s `sitemaps` framework. It helps search engines index key pages like products and static views.

### ✅ Included in Sitemap:
- Published products (`shop.ProductModel`)
- Static pages: Home, About, Contact, Newsletter (`website`)
- Multilingual support via `django-parler`

### 🔗 Access Sitemap:
Once the server is running, visit:
```
/sitemap.xml
```
---
## ⚠️ Error Handling

Custom error handlers are defined in the main URL configuration to gracefully handle common HTTP errors when `DEBUG = False`.

```python
handler404 = 'django.views.defaults.page_not_found'
handler403 = 'django.views.defaults.permission_denied'
handler500 = 'django.views.defaults.server_error'
```

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
