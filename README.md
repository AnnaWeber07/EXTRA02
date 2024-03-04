
---

# PAD

the project is designed to help manage user and content data. It uses PostgreSQL for users, MongoDB for content, Redis for caching, and has an endpoint for custom two-phase commit logic.

## How it Works

- **User Data**:
  - The API stores user data in a PostgreSQL database.
  - It creates a table called `users` if it's not already there, with columns for `id`, `name`, and `email`.
  - You can get all users, create new users, or update existing ones using `/users` endpoints.

- **Content Data**:
  - Content data is stored in a MongoDB collection called `content_collection`.
  - If the collection doesn't exist, the API creates it.
  - Endpoints like `/content` and `/mongo-data` let you get all content or add new content.

- **Redis Cache**:
  - Redis helps speed up user data retrieval.
  - When you request user data at `/users`, it checks Redis first before getting data from PostgreSQL and MongoDB.

- **Two-Phase Commit**:
  - There's a special `/two-phase-commit` endpoint for handling custom two-phase commit logic.
  - This is useful for managing complex transactions across different databases.

## How to Run

### What You Need
- Docker
- Docker Compose

### Steps

1. First, clone this repository.

2. **Important!** Before running the app, start the necessary containers:
   - Start PostgreSQL containers.
   - Start MongoDB containers.
   - Start Redis container.
   - 
3. Now, build and run the Flask API container:

4. Your API should be running at `http://localhost:5000`.

## Endpoints

- **GET /users**:
  - Gets all users from PostgreSQL and MongoDB.
  - Caches users in Redis for faster future requests.

- **POST /users**:
  - Adds a new user to the PostgreSQL database.

- **PUT /users**:
  - Updates an existing user's email in PostgreSQL.

- **GET /content**:
  - Retrieves all content from the MongoDB collection.

- **POST /mongo-data**:
  - Adds new data to the MongoDB collection.

- **PUT /content**:
  - Updates content with a specific title in MongoDB.

- **POST /two-phase-commit**:
  - Special endpoint for implementing custom two-phase commit logic.