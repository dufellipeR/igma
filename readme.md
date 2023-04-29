# IGMA

This project is a Django REST Framework (DRF) API built with Docker

## Requirements

To run this project, you'll need the following:

- Docker
- Docker Compose

## Overview

- Tests: *tests.py*
- Endpoints: *views.py*
- CPF Validator: *helpers.py*
- Schema: *models.py*

## Getting Started

1. Clone the repository:

    ```sh
    git clone https://github.com/dufellipeR/igma.git
    cd igma
    ```

2. Build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

3. Create the Django database tables:

    ```sh
    docker-compose exec server python manage.py migrate
    ```


5. The API should now be available at [http://localhost:8000/](http://localhost:8000/).

## Development

To start a development server:

1. Build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

2. Run Django's development server:

    ```sh
    docker-compose exec server python manage.py runserver 0.0.0.0:8000
    ```

3. The API should now be available at [http://localhost:8000/api/](http://localhost:8000/api/).

## Testing

To run the tests:

```sh
docker-compose exec server python manage.py test
```

Location: *tests.py*

## Configuration

### Environment Variables

This project uses environment variables to configure the database and other settings. For simplicity sake, the enviroment variables are already set on docker-compose.yml

## Technologies Used

This project was developed using the following technologies:

- Python 3.10.9
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL 13.3

The project also uses other libraries and tools that can be found in the `requirements.txt` file. 

For more information on how to run the project, please refer to the [Getting Started](#getting-started) section of this README.