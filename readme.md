# IGMA

This project is a Django REST Framework (DRF) API built with Docker

## Overview

- Tests: customer/tests.py
- Endpoints: customer/views.py
- CPF Validator: customer/helpers.py
- Schema: customer/models.py

## Requirements

To run this project, you'll need the following:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

    ```sh
    git clone https://github.com/dufellipeR/igma.git
    cd igma
    ```

2. Build and run the Docker containers:

    ```sh
    docker-compose up --build -d
    ```

3. Create the Django database tables:

    ```sh
    docker-compose exec server python manage.py migrate
    ```


4. The API should now be available at [http://localhost:8000/](http://localhost:8000/).
5. Docs should now be available
   at [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)


## Testing

To run the tests:

```sh
docker-compose exec server python manage.py test
```

## Configuration

### Environment Variables

This project uses environment variables to configure the database and other settings. For simplicity sake, the
enviroment variables are already set on docker-compose.yml

## Technologies Used

This project was developed using the following technologies:

- Python 3.10.9
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL 13.3

The project also uses other libraries and tools that can be found in the `requirements.txt` file.

For more information on how to run the project, please refer to the [Getting Started](#getting-started) section of this
README.