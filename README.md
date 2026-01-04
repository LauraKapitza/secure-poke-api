# SecurePokeAPI (WIP)

SecurePokeAPI is a Django REST Framework project that adds authentication and access control on top of the public [PokeAPI](https://pokeapi.co).  
Users must log in and join Pokémon type groups to access Pokémon data.

---

## Getting Started

1. Clone the repo
    ```bash
    git clone https://github.com/yourusername/securepokeapi.git
    cd securepokeapi
    ```
2. Create a virtual environment

    On Windows:
    ```bash
    python -m venv venv
    source venv\venv\Scripts\activate
    ```

    On Linux/Mac:
    ```bash
    python -m venv venv
    source venv/bin/activate # for Git Bash
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
   
4. Run migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
   
5. Create a superuser 
    ```bash
    python manage.py createsuperuser
    ```

6. Run the server
    ```bash
    python manage.py runserver
    ```
   
## Authentication Flow

1. Login with username & password via the endpoint `POST /api/login/`. Example: 
    ```json
    {
        "username": "admin",
        "password": "yourpassword"
    }
    ```
   Response:
    ```json
    {
        "access": "<JWT access token>",
        "refresh": "<JWT refresh token>"
    }
    ```
2. Use the token by copying the `access` token and including it in the headers:
    ```bash
    Authorization: Bearer <access_token>
    ```
   
## Testing endpoints

A Postman collection is included (`secure_poke_api_collection.json`). Import it into Postman (or another API platform)
and run the requests in order:
1. Login, then copy token
2. Set token in Authorization tab (Bearer Token)
3. Call `/user/me`, `/group/<pokemon_type>/add`, etc.

## Run tests

From the project root, execute the following command to run the tests for the Access Management API:
```bash
python manage.py test access_management_api
```

To run all tests from secure poke api project, use the following command:
```bash
python manage.py test
```

## Reflections

- using pytest for test files
- using postgresql as database for storing data
- storing pokemon types into d, and adding a cron job for updating the content (once a while)