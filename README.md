🛍️ Marjan Store – E-commerce API with Django REST Framework

**Live API:** [https://marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com)

Marjan Store is a fully functional e-commerce backend built with Django and Django REST Framework. It supports user authentication, product browsing, cart management, and order processing. The project also includes auto-generated API documentation using Swagger and ReDoc.

---

## 🚀 Features

- 🔐 JWT-based user authentication (register/login)
- 🛒 Product listing and detail views
- 🛍️ Cart management per user
- 📦 Order creation and history
- 🧑‍💼 Admin panel for product management
- 📚 Interactive API documentation (Swagger & ReDoc)

---

## 🧰 Tech Stack

- **Backend:** Django, Django REST Framework
- **Auth:** JWT (via `djangorestframework-simplejwt`)
- **Docs:** Swagger UI & ReDoc (`drf-yasg`)
- **Database:** PostgreSQL (or SQLite for local dev)
- **Deployment:** Render

---

## 📚 API Documentation

This project includes auto-generated API docs for developers:

| Tool | URL |
|------|-----|
| **Swagger UI** | [`/swagger/`](https://marjanrezaei-store.onrender.com/swagger/) |
| **Swagger JSON** | [`/swagger.json`](https://marjanrezaei-store.onrender.com/swagger.json) |
| **ReDoc** | [`/redoc/`](https://marjanrezaei-store.onrender.com/redoc/) |

These endpoints allow you to explore and test the API directly from your browser.

---

## 🛠️ Installation & Setup

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

### 5. Create superuser (optional for admin access)
```bash
python manage.py createsuperuser
```

### 6. Start the development server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 🔐 Authentication Flow

- Register: `POST /api/auth/register/`
- Login: `POST /api/auth/login/`
- Use the returned JWT token in the `Authorization` header:
  ```
  Authorization: Bearer <your_token>
  ```

---

## 📡 API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products/` | GET | List all products |
| `/api/products/<id>/` | GET | Retrieve product details |
| `/api/cart/` | GET/POST | View or add to cart |
| `/api/orders/` | GET/POST | View or create orders |
| `/api/auth/register/` | POST | Register a new user |
| `/api/auth/login/` | POST | Login and receive JWT token |

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Marjan Rezaei**  
GitHub: [@marjanrezaei](https://github.com/marjanrezaei)  
Live API: [marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com)

---

If you'd like, I can help you add badges (build status, license, deployment), or even a contributing guide for collaborators. Just say the word!
