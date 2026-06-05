from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "Fresh Start", "content": "Taking things one step at a time today. Progress, no matter how small, still counts."},
    {"id": 2, "title": "Quiet Wins", "content": "Not every achievement needs an audience. Some victories are best enjoyed in silence."},
]


def next_id(posts):
    """ Creates an unique id for a blog post. """
    current_ids = [item["id"] for item in posts]
    count = 1
    while True:
        new_id = count
        if new_id not in current_ids:
            return new_id
        count += 1


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        data = request.json
        try:
            title = data['title']
            content = data['content']

            new_post = {
                "id": next_id(POSTS),
                "title": title,
                "content": content,
            }
            POSTS.append(new_post)
            print("Added a new post. POSTS now has length", len(POSTS))

            return jsonify(new_post), 201

        except KeyError as e:
            return jsonify({ 'error': f'Required field {str(e)} not set.' }), 400
        

    return jsonify(POSTS), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
