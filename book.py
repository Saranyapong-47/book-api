from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  


MONGO_URI = "mongodb+srv://SXran:<password>@book-api.uxs7s.mongodb.net/?retryWrites=true&w=majority&appName=Book-API"
client = MongoClient(MONGO_URI)


db = client.book  
books_collection = db.book  

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    
    new_book = {
        "title": data["title"],
        "author": data["author"],
        "image_url": data["image_url"]
    }

    result = books_collection.insert_one(new_book)
    new_book["_id"] = str(result.inserted_id)  
    return jsonify(new_book), 201


@app.route('/books', methods=['GET'])
def get_all_books():
    books = list(books_collection.find({}))
    
    for book in books:
        book["_id"] = str(book["_id"])
    
    return jsonify({"books": books})


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    
    if book:
        book["_id"] = str(book["_id"])
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404


@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    
    result = books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": data})
    
    if result.matched_count:
        updated_book = books_collection.find_one({"_id": ObjectId(book_id)})
        updated_book["_id"] = str(updated_book["_id"])
        return jsonify(updated_book)
    else:
        return jsonify({"error": "Book not found"}), 404


@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = books_collection.delete_one({"_id": ObjectId(book_id)})
    
    if result.deleted_count:
        return jsonify({"message": "Book deleted successfully"})
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)