# Volume API

This project is a Django-based REST API with Swagger UI for documenting the API. The project includes an app named `volume_api` that contains a simple API endpoint.

## Setup Instructions

### Create and Activate a Virtual Environment

First, create a new virtual environment and activate it (can be Conda/PyCharm):

```bash
python -m venv myenv
```

### Install Dependencies
Install Django, Django REST framework, and drf-yasg for Swagger UI.
```bash
pip install -r requirements.txt
```

### Run Migrations and Start the Server
Apply migrations and start the development server.
```bash
python manage.py migrate
python manage.py runserver
python manage.py makemigrations # If changes happen for e.g. superuser
```

### Docker stack
Running commands inside Docker image:
```bash
docker-compose up --build
docker exec -it volume_api-volume_api-1 black .
docker exec -it volume_api-volume_api-1 python manage.py migrate
docker exec -it volume_api-volume_api-1 python manage.py makemigrations
```

### Add tiff file to serve as tiles
To add tiff file and viewed as tiles on frontend:
1. Go to 8000/admin
2. Login with admin username and password
3. Go to 'image-file' section and upload one

### Code Formatting with Black
To format your code with black, run the following command in your project directory:
```bash
black .
```