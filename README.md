Marjan Store – Django REST API E-commerce

GitHub Repository: https://github.com/marjanrezaei/marjanrezaei-store

Marjan Store is a RESTful e-commerce backend built with Django and Django REST Framework (DRF). It provides APIs for products, users, carts, and orders, making it suitable for web and mobile frontends.

🛠️ Features

RESTful API Endpoints: Full CRUD operations for products, carts, and orders.

User Authentication: JWT-based login and registration.

Admin Dashboard: Manage products, users, and orders.

Search & Filtering: Easily query products by category, name, or price.

Scalable Architecture: Designed to handle growing data and traffic.

🚀 Installation
Prerequisites

Python 3.8+

Django 3.2+

Django REST Framework

PostgreSQL (or SQLite for development)

Setup

Clone the repository:

git clone https://github.com/marjanrezaei/marjanrezaei-store.git
cd marjanrezaei-store


Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser:

python manage.py createsuperuser


Run the development server:

python manage.py runserver


Your API will be available at http://127.0.0.1:8000/api/.

📦 Docker Setup

Build Docker containers:

docker-compose build


Run the containers:

docker-compose up


The API is accessible at http://localhost:8000/api/.

🔧 API Endpoints
Endpoint	Method	Description
/api/products/	GET	List all products
/api/products/<id>/	GET	Retrieve product details
/api/products/	POST	Add new product (admin only)
/api/products/<id>/	PUT	Update product (admin only)
/api/products/<id>/	DELETE	Delete product (admin only)
/api/cart/	GET	View user cart
/api/cart/	POST	Add item to cart
/api/cart/<id>/	DELETE	Remove item from cart
/api/orders/	POST	Create a new order
/api/orders/<id>/	GET	Retrieve order details
/api/auth/register/	POST	User registration
/api/auth/login/	POST	User login (JWT token returned)
🛡️ Authentication & Permissions

JWT Authentication for secure API access

Admin users have full CRUD access

Regular users can manage their own carts and orders

🧪 Testing

Run tests with:

python manage.py test

📄 License

This project is licensed under the MIT License – see the LICENSE
 file for details.

📞 Contact

GitHub: marjanrezaei

Email: marjan.rezaei@example.com
