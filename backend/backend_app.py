from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "Fresh Start", "content": "Taking things one step at a time today. Progress, no matter how small, still counts."},
    {"id": 2, "title": "Quiet Wins", "content": "Not every achievement needs an audience. Some victories are best enjoyed in silence."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
