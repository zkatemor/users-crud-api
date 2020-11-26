# User's CRUD API with Bearer Auth

## Technology
- Python3
- Flask
- PostgreSQL

## How to

1. Create PostgreSQL database

2. Starting a project from IDE. Create .env file by example.
    
        virtualenv venv
        
        source venv/bin/activate
        
        pip install -r requirements.txt
        
        python manage.py db init
        
        python manage.py db migrate
        
        python manage.py db upgrade

3. Create line in token table in database

4. Run server
        
        python manage.py runserver

## API Documentation

### Auth

`POST` /api/v1/auth

**Body (json)**

- *username* (string) is required
- *password* (string) is required

**Example:**
```json
{
    "username": "rfnz",
    "password":"qwerty1234"
}
```

**Response**

- `422 Unprocessable Entity` 

```json
{
    "error": {
        "message": "The browser (or proxy) sent a request that this server could not understand."
    }
}
```

- `401 Unauthorized` 

```string
Unauthorized Access
```

```json
{
    "error": {
        "message": "The browser (or proxy) sent a request that this server could not understand."
    }
}
```

- `201 OK` 

```json
{
    "result": {
        "token": "cdf85a5de654d6519edf962009d89b43"
    }
}
```

### Create user

`POST` /api/v1/user

**Body (json)**

- *username* (string) is required
- *first_name* (string) is not required
- *last_name* (string) is not required
- *is_active* (boolean) is required

**Example:**
```json
{
    "username": "rfnz",
    "first_name":"Ekaterina",
    "last_name":"Zababurina",
    "is_active": true
}
```

**Response**

- `422 Unprocessable Entity` 

```json
{
    "error": {
        "message": "The browser (or proxy) sent a request that this server could not understand."
    }
}
```

- `401 Unauthorized` 

```string
Unauthorized Access
```

- `201 OK` 

```json
{
    "result": {
        "id": 3,
        "username": "zkatemor",
        "first_name": "Ekaterina",
        "last_name": "Zababurina",
        "is_active": true
    }
}
```

### Get a list of users

`GET` /api/v1/users

**Response**

- `422 Unprocessable Entity` 

```json
{
    "error": {
        "message": "The browser (or proxy) sent a request that this server could not understand."
    }
}
```

- `401 Unauthorized` 

```string
Unauthorized Access
```

- `200 OK` 

```json
{
    "result": [
        {
            "id": 1,
            "username": "rfnz",
            "first_name": "Ekaterina",
            "last_name": "Zababurina",
            "is_active": true
        },
        {
            "id": 2,
            "username": "qwerty",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "is_active": true
        }
    ]
}
```

### Get user details by ID

`GET` /api/v1/users/:id

**Body (in path)**

- *id* (string) is required

**Response**

- `404 Not Found` 

```json
{
    "error": {
        "message": "User not found"
    }
}
```

- `401 Unauthorized` 

```string
Unauthorized Access
```

- `200 OK` 

```json
{
    "result": {
        "id": 1,
        "username": "rfnz",
        "first_name": "Ekaterina",
        "last_name": "Zababurina",
        "is_active": true
    }
}
```

### Update user

`PUT` /api/v1/users/:id

**Body (in path)**

- *id* (string) is required

**Body (json)**

- *username* (string) is not required
- *first_name* (string) is not required
- *last_name* (string) is not required
- *is_active* (boolean) is not required

**Response**

- `404 Not Found` 

```json
{
    "error": {
        "message": "User not found"
    }
}
```

- `401 Unauthorized` 

```string
Unauthorized Access
```

- `200 OK` 

```json
{
    "result": {
        "id": 1,
        "username": "zkatemor",
        "first_name": "Ekaterina",
        "last_name": "Zababurina",
        "is_active": true
    }
}
```

### Delete user

`DELETE` /api/v1/users/:id

**Body (in path)**

- *id* (string) is required

**Response**

- `404 Not Found` 

```json
{
    "error": {
        "message": "User not found"
    }
}
```

- `401 Unauthorized` 

```string
Unauthorized Access
```

- `200 OK` 

```json
{
    "success": true
}
```
