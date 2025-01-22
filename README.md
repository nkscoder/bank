# Account Management API

This project is a Django-based RESTful API for managing user accounts, including account creation, login, and retrieval of account details. The API is built using the Django Rest Framework (DRF) and leverages JWT for authentication. Additionally, the project integrates with RabbitMQ to communicate with an ATM system.

## Features

- **Account Creation**: Allows users to create an account with an email, password, account number, and PIN.
- **Login**: Allows users to log in with email and password, and receive JWT tokens for authentication.
- **Account Details**: Retrieves account details for authenticated users.
- **RabbitMQ Integration**: Sends account data to a RabbitMQ queue for ATM updates.

## Technologies

- Django 5.1.5
- Django Rest Framework 3.15.2
- djangorestframework_simplejwt 5.4.0
- RabbitMQ for message queuing
- PostgreSQL for the database

## Installation

### Prerequisites

- Python 3.8 or later
- PostgreSQL Database
- RabbitMQ (for message queuing)

### Step-by-Step Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/nkscoder/bank.git
    cd bank
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up the database:

    - Ensure you have PostgreSQL installed and running.
    - Create a database and configure your database settings in `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

6. Run migrations:

    ```bash
    python manage.py migrate
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

8. (Optional) Set up RabbitMQ:

    - Install RabbitMQ on your local machine or use a cloud service.
    - Ensure RabbitMQ is running on `localhost`.

## API Endpoints

### 1. **Create Account**
- **URL**: `/api/create_account/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "password123",
        "account_number": "1234567890",
        "pin": "1234"
    }
    ```
- **Response**:
    ```json
    {
        "account": {
            "user": 1,
            "account_number": "1234567890",
            "pin": "1234",
            "balance": 0.0
        },
        "access_token": "jwt_access_token",
        "refresh_token": "jwt_refresh_token"
    }
    ```

### 2. **Login**
- **URL**: `/api/login/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```
- **Response**:
    ```json
    {
        "access_token": "jwt_access_token",
        "refresh_token": "jwt_refresh_token"
    }
    ```

### 3. **Get Account Details**
- **URL**: `/api/account_details/`
- **Method**: `GET`
- **Authentication**: JWT Token required (Include `Authorization: Bearer <access_token>` header)
- **Response**:
    ```json
    {
        "user": 1,
        "account_number": "1234567890",
        "pin": "1234",
        "balance": 0.0
    }
    ```

## RabbitMQ Integration

The API sends account information to RabbitMQ whenever a new account is created. This is done in the `create_account` view where it sends the account number, PIN, and balance data to the `atm_queue` for further processing (e.g., ATM updates).

### Configuration

- RabbitMQ is expected to be running locally (`localhost`), but this can be configured in the `send_to_rabbitmq` function in `utils.py`.

## Testing

You can test the API using tools like [Postman](https://www.postman.com/) or `curl`.

### Example cURL Commands:

1. **Create Account**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/create_account/ \
        -H "Content-Type: application/json" \
        -d '{"email": "user@example.com", "password": "password123", "account_number": "1234567890", "pin": "1234"}'
    ```

2. **Login**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/login/ \
        -H "Content-Type: application/json" \
        -d '{"email": "user@example.com", "password": "password123"}'
    ```

3. **Get Account Details**:
    ```bash
    curl -X GET http://127.0.0.1:8000/api/account_details/ \
        -H "Authorization: Bearer <access_token>"
    ```

## Dependencies

- `asgiref==3.8.1`
- `django==5.1.5`
- `djangorestframework==3.15.2`
- `djangorestframework_simplejwt==5.4.0`
- `pika==1.3.2`
- `psycopg2==2.9.10`
- `python-dotenv==0.21.1`

You can install the required dependencies with the following command:

```bash
pip install -r requirements.txt
