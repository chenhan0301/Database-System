from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection (adjust as per your local MongoDB setup)
client = MongoClient('mongodb://localhost:27017/')
db = client['local']  # The database name
collection = db['startup_log']  # The collection name

@app.route('/')
def index():
    # Fetch all documents from the startup_log collection
    data = list(collection.find({}))
    # Convert MongoDB documents to JSON-friendly format
    for doc in data:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string for HTML rendering

    return render_template('index.html', data=data)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get form data from request
        name = request.form.get('name')
        description = request.form.get('description')

        # Insert the new document into the MongoDB collection
        new_doc = {'name': name, 'description': description}
        collection.insert_one(new_doc)

        # Redirect to the index page after successful insertion
        return redirect(url_for('index'))

    # If GET request, show the create form
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)