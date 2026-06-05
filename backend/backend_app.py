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


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
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


@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post_id = int(post_id)

    try:
        old_len = len(POSTS)
        POSTS = [p for p in POSTS if p["id"] != post_id]
        new_len = len(POSTS)

        assert new_len == old_len - 1
            
        return jsonify({ 'message': f'Post with id {post_id} has been deleted successfully.'}), 200
    
    except AssertionError:
        return jsonify({ 'error': 'Post not found.' }), 404

    except ValueError:
        return jsonify({ 'error': 'Invalid post id.'}), 400


@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post_id = int(post_id)

        post = [p for p in POSTS if p['id'] == post_id][0]

        data = request.json

        valid_fields = ['title', 'content']
        at_least_one_valid_field = False

        for key in data:
            if key in valid_fields:
                post[key] = data[key]
                at_least_one_valid_field = True

        if not at_least_one_valid_field:
            raise TypeError
            
        return jsonify(post), 200

    except TypeError:
        return jsonify({ 'error': f'Expected at least one of valid fields: {valid_fields}' }), 400

    except IndexError:
        return jsonify({ 'error': 'Post not found.' }), 404

    except ValueError:
        return jsonify({ 'error': 'Invalid post id.' }), 400


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    posts = POSTS
    title = request.args.get('title')
    content = request.args.get('content')

    if title:
        posts = [p for p in posts if title.lower() in p['title'].lower()]

    if content:
        posts = [p for p in posts if content.lower() in p['content'].lower()]

    return jsonify(posts), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
