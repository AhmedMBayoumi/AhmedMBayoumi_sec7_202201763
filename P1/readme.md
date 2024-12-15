# Book Library API

A Flask-based API for managing a book library. Allows users to add, update, delete, and search books.

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## Building and Running the Docker Container

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AhmedMBayoumi/P1
   cd P1
   ```
2. **Build the Docker image**:
```bash
    docker build -t book-library-api .
```
3. **Run the Docker container**:
```bash
docker run -p 5000:5000 book-library-api

Verify the API:

Access http://localhost:5000 to confirm the API is running.
```

## Accessing the Swagger API Documentation

After running the Docker container, open the Swagger UI at:

```bash
http://localhost:5000/apidocs
```

From there, you can interact with API endpoints like:

- `GET /books`: List all books
- `POST /books`: Add a new book
- `GET /books/search`: Search books by `author`, `published_year`, or `genre`
- `DELETE /books/{isbn}`: Delete a book by ISBN
- `PUT /books/{isbn}`: Update a book by ISBN
