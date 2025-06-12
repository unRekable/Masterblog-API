from urllib import request

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        if not request.json or not 'title' in request.json or not 'content' in request.json:
            return jsonify({"error": "Missing title or content"}), 400

        new_id = max([post['id'] for post in POSTS]) + 1
        title = request.json['title']
        content = request.json['content']

        new_post = {"id": new_id, "title": title, "content": content}
        POSTS.append(new_post)

        return jsonify(new_post), 201
    else:
        return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
