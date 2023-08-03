from flask import *
from flask_cors import CORS
from get_database import get_database

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
CORS(app, origins="http://localhost:5173")

@app.route("/")
def index():
    return "Hello, world!"

@app.route("/fetch_all_photos")
def fetch_all_photos():
    db = get_database('exchange_japan')
    collection = db.photos
    data = list(collection.find({}, {"_id": 0}).limit(10))
    return jsonify(data)

@app.route("/fetch_photo/", methods=['GET'])
def fetch_photo():
    name = request.args.get('name')
    print(f"Received name parameter: {name}")

    db = get_database('exchange_japan')
    collection = db.photos
    data = collection.find_one({'name': name}, {"_id": 0})
    print(f"Result from database: {data}")

    if data is None:
        # 如果找不到對應的照片資料，回傳 404 錯誤
        return jsonify({'error': 'Photo not found'}), 404
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=3000)