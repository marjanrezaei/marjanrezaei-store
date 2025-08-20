# Marjan Store – E-commerce API (Django REST Framework)

🚀 **Live API:** [https://marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com)

Marjan Store is an **API-based e-commerce backend** built with **Django REST Framework (DRF)**.
It provides a complete RESTful API for managing products, users, shopping carts, and orders.
The project is deployed on **Render**, so you can directly interact with the API endpoints online.

---

## ✨ Features

* 🔑 **Authentication & Authorization**

  * User registration & login
  * JWT-based authentication for secure API access

* 🛍️ **Product Management**

  * List, search, and filter products
  * Admin-only endpoints for creating, updating, and deleting products

* 🛒 **Shopping Cart**

  * Add, update, and remove items from the cart
  * Retrieve cart details per user

* 📦 **Order Management**

  * Create orders from cart
  * View user-specific order history

* ⚡ **API-first Design**

  * Built entirely on DRF for use with web frontends, mobile apps, or third-party integrations

---

## 🌍 Live API on Render

The backend is deployed and accessible here:
👉 [https://marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com)

### Example Endpoints

| Endpoint              | Method | Description                |
| --------------------- | ------ | -------------------------- |
| `/api/products/`      | GET    | List all products          |
| `/api/products/<id>/` | GET    | Get single product details |
| `/api/auth/register/` | POST   | Register a new user        |
| `/api/auth/login/`    | POST   | Login & get JWT token      |
| `/api/cart/`          | GET    | View cart for current user |
| `/api/cart/`          | POST   | Add product to cart        |
| `/api/orders/`        | POST   | Create a new order         |
| `/api/orders/`        | GET    | List user’s past orders    |

---

## ⚙️ Local Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/marjanrezaei/marjanrezaei-store.git
   cd marjanrezaei-store
   ```

2. **Create a virtual environment & activate it**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server**

   ```bash
   python manage.py runserver
   ```

Now open: `http://127.0.0.1:8000`

---

## 🧪 Testing

Run unit tests with:

```bash
python manage.py test
```

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

* GitHub: [marjanrezaei](https://github.com/marjanrezaei)
* Live API: [marjanrezaei-store.onrender.com](https://marjanrezaei-store.onrender.com) 
