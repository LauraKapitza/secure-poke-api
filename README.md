# Secure Poke API

Secure Poke API is a Django REST Framework project that adds authentication and access control on top of the public [PokeAPI](https://pokeapi.co).  
Users must log in and join Pokémon type groups to access Pokémon data based on their assigned types.

## Table of Contents

- [Getting Started](#getting-started)
- [Authentication Flow](#authentication-flow)
- [API Endpoints](#api-endpoints)
  - [Access Management API](#access-management-api)
    - [User Info](#1-user-info-get-apiuserme)
    - [Add a Pokémon Type Group](#2-add-a-pokémon-type-group-post-apigrouppokemontypeadd)
    - [Remove a Pokémon Type Group](#3-remove-a-pokémon-type-group-post-apigrouppokemontyperemove)
  - [Pokémon API](#pokémon-api)
    - [List Accessible Pokémon](#1-list-accessible-pokémon-get-apipokemon)
    - [Get Pokémon Details](#2-get-pokémon-details-get-apipokemonidorname)
- [Testing Endpoints](#testing-endpoints)
- [Run Tests](#run-tests)
- [Reflections & Future Improvements](#reflections--future-improvements)
  - [Pagination for Large Pokémon Lists](#pagination-for-large-pokémon-lists)
  - [Migrating to-pytest](#migrating-to-pytest)
  - [Using-postgresql-as-database](#using-postgresql-as-the-database)
  - [Storing-pokémon-types-in-the-database](#storing-pokémon-types-in-the-database)
  - [Implementing-openapi-documentation](#implementing-openapi-documentation)

---

## Getting Started

1. Clone the repository
    ```bash
    git clone https://github.com/yourusername/secure-poke-api.git
    cd secure-poke-api
    ```
2. Create a virtual environment

    On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    On Linux/Mac:
    ```bash
    python -m venv venv
    source venv/bin/activate
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

6. Start the server
    ```bash
    python manage.py runserver
    ```
   
## Authentication Flow

1. Login with username & password via the endpoint `POST /api/login/`. 

   Request:
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
2. Use the token by copying the `access` token and including it in all protected requests:
    ```bash
    Authorization: Bearer <access_token>
    ```
 
## API Endpoints

### Access Management API

#### 1. User Info: `GET /api/user/me/`

Returns the authenticated user’s details.

Example Response:
```json
{
  "id": 1,
  "username": "admin",
  "groups": ["fire", "water"]
}
```

#### 2. Add a Pokémon type group: `POST /api/group/<pokemon_type>/add/`

Adds a Pokémon type group to the user's profile.

Example Request: 
```
POST /api/group/fire/add/
```

Example Response:
```json
{ "message": "Added fire group" }
```


#### 3. Remove a Pokémon type group: `POST /api/group/<pokemon_type>/remove/`

Removes a given Pokémon type group to the user's profile.

Example Request: 
```
POST /api/group/fire/remove/
```

Example Response:
```json
{ "message": "Removed fire group" }
```

### Pokémon API

#### 1. List accessible Pokémon: `GET /api/pokemon/`

Returns all Pokémon whose types match the user’s groups.

Example Response:
```json
[
  { "name": "charmander", "url": "/api/pokemon/charmander/" },
  { "name": "vulpix", "url": "/api/pokemon/vulpix/" }
]
```

#### 2. Get Pokémon details: `GET /api/pokemon/<id_or_name>/`

Returns details of a Pokémon whose types match the user’s groups.

Example Request:
```
GET /api/pokemon/charmander/
```

Example Response for valid request:
```json
{
  "id": 4,
  "name": "charmander",
  "types": [
    { "slot": 1, "type": { "name": "fire" } }
  ],
  "height": 6,
  "weight": 85,
  "stats": [...],
  "abilities": [...],
  "sprites": {...}
}
```

Example Response for invalid request:
```json
{
  "error": "Forbidden: you do not have access to this Pokémon"
}

```


## Testing endpoints

An API endpoint collection is included (`secure_poke_api_collection.json`). Import it into Postman (or another API platform),
and run the requests in order:
1. Login, then copy token
2. Set token in Authorization tab (Bearer Token)
3. Call `/user/me`, `/group/<pokemon_type>/add`, etc.

## Run tests

From the project root, you can run all tests from the apps `access_management_api` and `pokemon_api`:
```bash
python manage.py test
```

You can also run the tests of a specific app by adding its name at the end of the test command:
```bash
python manage.py test <app-name> # e.g. access_management_api
```

## Reflections & Future Improvements

### Pagination for large Pokémon lists

The GET endpoint `/api/pokemon/` may return hundreds of entries if a user belongs to many type groups. 
Adding pagination would improve performance and reduce response size.

### Migrating to pytest
Pytest offers features such as fixtures and parametrization which help to simplify the process
of writing and executing tests.
Migrating the test suite would make it more maintainable and expressive.

### Using PostgreSQL as the database
SQLite is fine for development, but PostgreSQL provides better performance, 
concurrency handling, and indexing for production environments.

### Using a Static Pokémon Type List vs. Database Storage

Currently, the system fetches types from the PokéAPI at runtime. 
However, Pokémon types rarely change, making a regular scheduled sync unnecessary. Two better alternatives include:

- Static List: Using a hardcoded list within the application code. This is sufficient given the infrequent updates to the Pokémon franchise and would significantly reduce external API overhead.
- Database Storage: Storing types in a local database table. This provides the best stability and allows for relational integrity within the app. A management command could be implemented to allow administrators to manually refresh the type list whenever a new generation of Pokémon is released.

### Implementing OpenAPI documentation

For an API that continues to grow, OpenAPI documentation (e.g., Swagger) helps maintain a clear overview of all endpoints and improves communication between developers.