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
        sort_key = request.args.get('sort')
        if sort_key not in ['title', 'content']:
            sort_key = None
        if sort_key:
            direction = request.args.get('direction', 'asc')
            reverse_order = (direction == 'desc')
            return jsonify(sorted(POSTS, key=lambda post: post[sort_key].lower(), reverse=reverse_order)), 200
        else:
            return jsonify(POSTS), 200

@app.route('/api/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def post_by_id(id):
    post = next((p for p in POSTS if p['id'] == id), None)

    if post is None:
        return jsonify({"error": "Post not found"}), 404

    if request.method == 'GET':
        return jsonify(post), 200

    if request.method == 'DELETE':
        POSTS.remove(post)
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200

    if request.method == 'PUT':
        title = request.json['title']
        content = request.json['content']

        post["title"] = title
        post["content"] = content

        return jsonify(post), 200

@app.route('/api/search', methods=['GET'])
def search():
    title_query = request.args.get('title', None)
    content_query = request.args.get('content', None)

    if title_query is None and content_query is None:
        return jsonify({"error": "Missing title or content"}), 400

    results = POSTS[:]

    if title_query:
        results = [
            post for post in results
            if title_query.lower() in post['title'].lower()
        ]

    if content_query:
        results = [
            post for post in results
            if content_query.lower() in post['content'].lower()
        ]

    if results:
        return jsonify(results), 200
    else:
        return jsonify({"error": "Post not found"}), 404

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
