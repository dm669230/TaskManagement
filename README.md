<!-- setup frontend -->
# Create frontend project
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install react-router-dom axios
npm run dev

<!-- Backend1 (Node.js Auth API) -->
# Create backend1 folder
cd ..
mkdir backend1
cd backend1

# Initialize Node.js project
npm init -y
npm install express bcryptjs jsonwebtoken sqlite3 cors body-parser

# Create files:
type nul > app.js 
type nul > db.js 
type nul > routes.js

<!-- Backend2 (Django + Django REST Framework) -->
# Create Django Project
cd ..
django-admin startproject backend2
cd backend2

# Create App
python manage.py startapp tasks

# Install needed libraries
pip install djangorestframework pandas openpyxl django-cors-headers

# Add to settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'tasks',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Allow React
CORS_ALLOW_ALL_ORIGINS = True

{
  "username": "vaibhav",
  "password": "securePassword123"
}

{
  "username": "dm@gmail.com",
  "password": "securePassword1234"
}

{
  "username": "dm669230@gmail.com",
  "password": "securePassword1234"
}


<!-- task_add -->
{
    "title":"debug",
    "status": "complete",
    "description": "Router path for /task_add bug fixed in backend2",
    "etc": 2,
    "due_date":"01-04-2025"
 }

{
  username: 'vsrivastava058@gmail.com',
  password: 'securePassword1234'
}