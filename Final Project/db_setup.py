# db_setup.py
from pymongo import MongoClient

def initialize_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['LibrarySystem']
    
    # 創建集合
    db.create_collection('Books')
    db.create_collection('Users')
    db.create_collection('Loans')
    
    # 插入一些範例資料
    db.Books.insert_many([
        {"title": "MongoDB Guide", "author": "John Doe", "category": "Technology"},
        {"title": "Python Basics", "author": "Jane Smith", "category": "Programming"},
    ])
    
    db.Users.insert_many([
        {"username": "user1", "borrow_history": []},
        {"username": "user2", "borrow_history": []},
    ])
    
    print("資料庫初始化完成！")

if __name__ == "__main__":
    initialize_db()
