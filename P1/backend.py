# To access Swagger UI, go to http://localhost:5000/apidocs/

from flask import Flask, request, jsonify, send_from_directory, render_template
from flasgger import Swagger


app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(app)

books = []

def find_book(isbn):
    return next((book for book in books if book['isbn'] == isbn), None)

@app.route('/')
def server():
    """
    the main HTML page.
    ---
    responses:
      200:
        description: Returns the index.html page
    """
    return render_template('index.html')

@app.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book to the collection.
    ---
    parameters:
      - name: book
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: The title of the book
            author:
              type: string
              description: The author of the book
            published_year:
              type: integer
              description: The published year of the book
            isbn:
              type: string
              description: The ISBN of the book
            genre:
              type: string
              description: The genre of the book
    responses:
      201:
        description: Book added successfully
      400:
        description: Missing required fields or book already exists
    """
    data = request.get_json()
    required_fields = ['title', 'author', 'published_year', 'isbn']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    if find_book(data['isbn']):
        return jsonify({"error": "Book with this ISBN already exists"}), 400

    book = {
        "title": data['title'],
        "author": data['author'],
        "published_year": data['published_year'],
        "isbn": data['isbn'],
        "genre": data.get('genre', None)
    }

    books.append(book)
    return jsonify({"message": "Book added successfully", "book": book}), 201

@app.route('/books', methods=['GET'])
def list_books():
    """
    List all books in the collection.
    ---
    responses:
      200:
        description: A list of all books
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
              author:
                type: string
              published_year:
                type: integer
              isbn:
                type: string
              genre:
                type: string
    """
    return jsonify(books), 200

@app.route('/books/search', methods=['GET'])
def search_books():
    """
    Search for books by author, published year, or genre.
    ---
    parameters:
      - name: author
        in: query
        type: string
        description: The author of the book to search for
      - name: published_year
        in: query
        type: integer
        description: The published year of the book to search for
      - name: genre
        in: query
        type: string
        description: The genre of the book to search for
    responses:
      200:
        description: A list of books matching the search criteria
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
              author:
                type: string
              published_year:
                type: integer
              isbn:
                type: string
              genre:
                type: string
    """
    author = request.args.get('author')
    published_year = request.args.get('published_year')
    genre = request.args.get('genre')

    filtered_books = books

    if author:
        filtered_books = [book for book in filtered_books if book['author'].lower() == author.lower()]
    if published_year:
        filtered_books = [book for book in filtered_books if book['published_year'] == published_year]
    if genre:
        filtered_books = [book for book in filtered_books if book.get('genre', '').lower() == genre.lower()]

    return jsonify(filtered_books), 200

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Delete a book by ISBN.
    ---
    parameters:
      - name: isbn
        in: path
        type: string
        description: The ISBN of the book to delete
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
    """
    global books
    book = find_book(isbn)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    books = [b for b in books if b['isbn'] != isbn]
    return jsonify({"message": "Book deleted successfully"}), 200

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    """
    Update a book's information by ISBN.
    ---
    parameters:
      - name: isbn
        in: path
        type: string
        description: The ISBN of the book to update
      - name: book
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            genre:
              type: string
    responses:
      200:
        description: Book updated successfully
      404:
        description: Book not found
    """
    data = request.get_json()
    book = find_book(isbn)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    for key in ['title', 'author', 'published_year', 'genre']:
        if key in data:
            book[key] = data[key]

    return jsonify({"message": "Book updated successfully", "book": book}), 200

if __name__ == '__main__':
    app.run(debug=True)
