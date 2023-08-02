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
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=3000)