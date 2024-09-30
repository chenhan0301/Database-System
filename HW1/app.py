from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL 連接設定
db_config = {
    'user': 'root',
    'password': '930301',
    'host': 'localhost',  # 或你的 MySQL 伺服器
    'database': 'testdb',
}

# 連接資料庫
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# 顯示學生資料
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 查詢現有資料，使用 studentinfo 表格
    query = "SELECT * FROM studentinfo"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', data=data)

# 新增學生資料
@app.route('/add', methods=['POST'])
def add_person():
    name = request.form['name']
    age = request.form['age']
    city = request.form['city']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 插入新資料到 studentinfo 表格
    query = "INSERT INTO studentinfo (name, age, city) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, age, city))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))

# 更新學生資料
@app.route('/update/<int:id>', methods=['POST'])
def update_person(id):
    name = request.form['name']
    age = request.form['age']
    city = request.form['city']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 更新資料，指定 studentinfo 表格
    query = "UPDATE studentinfo SET name=%s, age=%s, city=%s WHERE id=%s"
    cursor.execute(query, (name, age, city, id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))

# 刪除學生資料
@app.route('/delete/<int:id>', methods=['GET'])
def delete_person(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 刪除資料，使用 studentinfo 表格
    query = "DELETE FROM studentinfo WHERE id=%s"
    cursor.execute(query, (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)