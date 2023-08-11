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
    page_num = int(request.args.get('page'))
    page_size = 50
    skip_count = (page_num - 1) * page_size

    db = get_database('exchange_japan')
    collection = db.photos
    data = list(collection.find({}, {"_id": 0}).sort("iso_date", 1).skip(skip_count).limit(page_size))
    return jsonify(data)
    db.close()

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
    db.close()

@app.route("/update_photo/", methods=['POST'])
def update_photo():
    try:
        data = request.json
        db = get_database('exchange_japan')
        collection = db.photos
        query = {'name': data['name']}
        collection.update_one(query, {'$set':
            {
                'description': data['description'],
                'colors': data['colors'],
                'places': data['places']
            }
        })
        print(f"已經更新{data['name']}的資料到資料庫")
        return jsonify({
            "message": "資料更新成功",
            "data": data
        })
    except Exception as e:
        # 如果發生錯誤，回傳錯誤訊息
        return jsonify({"error": str(e)}), 500
    db.close()

if __name__ == "__main__":
    app.run(port=3000)