# Flask Blog App

A simple blog application built using Flask, featuring user authentication, CRUD operations for blog posts, and a clean project structure for learning and development.

## Features
- User authentication (Signup, Login, Logout)
- Create, Read, Update, and Delete (CRUD) operations for blog posts
- Commenting system (optional)
- Responsive UI with Bootstrap
- Secure password hashing with Flask-Bcrypt
- Database migrations using Flask-Migrate

## Project Structure
```plaintext
flask-blog-app/
│── app/
│   ├── __init__.py          # Flask app factory
│   ├── extensions.py        # Initialize extensions (SQLAlchemy, JWT, etc.)
│   ├── models/              # Database models
│   │   ├── __init__.py      # Initialize models
│   │   ├── user.py          # User model
│   │   ├── post.py          # Blog post model
│   │   ├── comment.py       # Comment model
│   ├── routes/              # Routes (views/controllers)
│   │   ├── __init__.py      # Blueprint registration
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Blog post routes
│   │   ├── user.py          # User profile routes (optional)
│   ├── templates/           # HTML templates
│   │   ├── auth/            # Auth-related templates
│   │   ├── blog/            # Blog post templates
│   ├── static/              # CSS, JS, images
│   │   ├── css/             # CSS
│   │   ├── js/              # js
│   │   ├── img/             # images
│── migrations/              # Flask-Migrate files
│── config/                  # Configurations
│   ├── __init__.py
│   ├── development.py       # Development config
│   ├── production.py        # Production config
│── run.py                   # Entry point to run Flask app
│── requirements.txt         # Project dependencies
│── .env                     # Environment variables
│── .gitignore               # Ignore unnecessary files
│── README.md                # Project documentation

```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/jayachandragoteti/Flask-Blog-App.git
   cd flask-blog-app
   ```
2. Create a virtual environment:
   ```sh
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
   - Windows:
     ```sh
     venv\Scripts\activate
     ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Set up the database:
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
6. Run the application:
   ```sh
   flask run
   ```

## Usage
- Navigate to `http://127.0.0.1:5000/`
- Sign up or log in to create and manage blog posts
- Edit or delete posts from your dashboard

## License
This project is licensed under the MIT License.

