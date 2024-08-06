# Volume API

This project is a Django-based REST API with Swagger UI for documenting the API. The project includes an app named `volume_api` that contains a simple API endpoint.

## Setup Instructions

### Prerequisites

It is recommended to have Docker and WSL2 (Windows Subsystem for Linux 2) prepared for a smoother development and deployment experience.

1. Docker

Install Docker from the official website.
Ensure Docker is running by executing docker --version in your terminal.

2. WSL2 (For Windows users):

Install WSL2 by following the instructions from the Microsoft documentation.
Ensure you have a Linux distribution installed and set to WSL2.

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
docker exec -it volume_api_app-volume_api-1 black .
docker exec -it volume_api-volume_api-1 python manage.py migrate
docker exec -it volume_api-volume_api-1 python manage.py makemigrations
```

### Add tiff file to serve as tiles
To add a TIFF file and view it as tiles on the frontend:

1. Go to http://localhost:8000/api/geotiffs/
2. Use the API endpoint to upload the TIFF file.

### API Documentation
For detailed API documentation and as the source of truth for all APIs, visit:
http://localhost:8000/swagger/

### Code Formatting with Black
To format your code with black, run the following command in your project directory:
```bash
black .
```

### CORS Headers not found in Geoserver responses?
Wait for your geoserver to spin up successfully, then perform:
```bash
docker cp ./web.xml volume_api_app-geoserver-1:/opt/apache-tomcat-9.0.86/webapps/geoserver/WEB-INF/web.xml
```