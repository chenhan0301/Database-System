from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

# 初始化 Flask 應用
app = Flask(__name__)

# 連接到 MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['LibrarySystem']
    print("✅ MongoDB connected")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
    exit()

# 首頁
@app.route('/')
def index():
    return render_template('index.html')

# 書籍管理頁面
@app.route('/books')
def books():
    try:
        # 查詢 MongoDB 中的書籍
        books = list(db.Books.find())
        for book in books:
            book['_id'] = str(book['_id'])  # 將 ObjectId 轉為字串
        return render_template('books.html', books=books)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 用戶管理頁面
@app.route('/users')
def users():
    try:
        # 假設從 MongoDB 查詢用戶資料
        users = list(db.Users.find())
        for user in users:
            user['_id'] = str(user['_id'])  # 將 ObjectId 轉為字串
        return render_template('users.html', users=users)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 新增用戶 API
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    db.Users.insert_one(data)
    return jsonify({"status": "success"})

# 刪除用戶 API
@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # 確保 user_id 是有效的 ObjectId
        if not ObjectId.is_valid(user_id):
            return jsonify({"status": "error", "message": "Invalid user ID"}), 400
        
        # 刪除指定的用戶
        result = db.Users.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({"status": "error", "message": "User not found"}), 404
        
        return jsonify({"status": "success", "message": "User deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 借閱記錄頁面
@app.route('/loans')
def loans():
    try:
        # 假設從 MongoDB 查詢借閱記錄資料
        loans = list(db.Loans.find())
        for loan in loans:
            loan['_id'] = str(loan['_id'])  # 將 ObjectId 轉為字串
            loan['book_id'] = str(loan['book_id'])  # 假設 `book_id` 也是 ObjectId，轉為字串
            loan['user_id'] = str(loan['user_id'])  # 假設 `user_id` 也是 ObjectId，轉為字串
        return render_template('loans.html', loans=loans)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 新增書籍 API
@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        # 接收新增書籍的 JSON 資料
        data = request.get_json()
        if not data or not all(key in data for key in ('title', 'author', 'category')):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # 插入書籍到 MongoDB
        result = db.Books.insert_one({
            "title": data['title'],
            "author": data['author'],
            "category": data['category']
        })
        return jsonify({"status": "success", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 刪除書籍 API
@app.route('/delete_book/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # 確保 book_id 是有效的 ObjectId
        if not ObjectId.is_valid(book_id):
            return jsonify({"status": "error", "message": "Invalid book ID"}), 400
        
        # 刪除指定的書籍
        result = db.Books.delete_one({"_id": ObjectId(book_id)})
        
        if result.deleted_count == 0:
            return jsonify({"status": "error", "message": "Book not found"}), 404
        
        return jsonify({"status": "success", "message": "Book deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 更新書籍 API
@app.route('/update_book/<book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        # 接收更新書籍的 JSON 資料
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        # 更新書籍資料
        result = db.Books.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"status": "error", "message": "Book not found"}), 404
        return jsonify({"status": "success", "message": "Book updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 搜尋書籍 API
@app.route('/search_books', methods=['GET'])
def search_books():
    try:
        # 接收搜尋的關鍵字
        query = request.args.get('query', '')
        if not query:
            return jsonify({"status": "error", "message": "Query is empty"}), 400

        # 在書籍中進行模糊搜尋
        books = list(db.Books.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }))

        for book in books:
            book['_id'] = str(book['_id'])  # 將 ObjectId 轉為字串
        return jsonify({"status": "success", "books": books}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 刪除借閱記錄 API
@app.route('/delete_loan/<loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    try:
        # 確保 loan_id 是有效的 ObjectId
        if not ObjectId.is_valid(loan_id):
            return jsonify({"status": "error", "message": "Invalid loan ID"}), 400
        
        # 刪除指定的借閱記錄
        result = db.Loans.delete_one({"_id": ObjectId(loan_id)})
        
        if result.deleted_count == 0:
            return jsonify({"status": "error", "message": "Loan record not found"}), 404
        
        return jsonify({"status": "success", "message": "Loan record deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
