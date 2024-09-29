# Assignment Django Project

This is a Django project for transforming JSON data based on field mappings. The project includes a flexible transformer function that takes input JSON data and modifies field names based on the provided mappings, while preserving the JSON structure.

## Requirements

- Python 3.8+
- Django 3.2+
- Git

## Setup Instructions

### Step 1: Clone the Repository

To clone the repository:

### Step 2: Create and Activate a Virtual Environment
  # For Linux/macOS
  python3 -m venv venv
  source venv/bin/activate
  
  # For Windows
  python -m venv venv
  venv\Scripts\activate

### Step 3: Install Dependencies
  pip install -r requirements.txt
### Step 4: Apply Migrations
  python manage.py makemigrations

  python manage.py migrate

  python manage.py createsuperuser

  python manage.py runserver

  

