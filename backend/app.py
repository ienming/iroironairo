from flask import *
from get_database import get_database
# db = get_database()
# collections = db.list_collection_names()

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

@app.route("/")
def index():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(port=3000)