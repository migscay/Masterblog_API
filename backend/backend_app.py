from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    if data["title"] == "" or data["content"] == "":
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        # Get the new post data from the client
        new_post = request.get_json()

        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400

        # Generate a new ID for the book
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        # Add the new book to our list
        POSTS.append(new_post)

        # Return the new book data to the client
        return jsonify(new_post), 201
    else:
        # if sorting was specified
        post_sorting = request.args.get('sort')
        post_direction = request.args.get('direction')
        print(post_sorting)
        print(post_direction)

        sorted_posts = POSTS

        if post_sorting:
            if not post_direction or post_direction == 'ASC':
                sorted_posts = sorted(POSTS, key=lambda x: x['title'], reverse=False)
            else:
                sorted_posts = sorted(POSTS, key=lambda x: x['title'], reverse=True)

        return jsonify(sorted_posts)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    search_term = request.args.get('title')
    post_search_result = [val for val in POSTS if search_term.casefold() in val['title'].casefold()]
    return jsonify(post_search_result)


def find_post_by_id(post_id):
    post_by_id = next((post for post in POSTS if post["id"] == int(post_id)), None)
    return post_by_id


@app.route('/api/posts/<int:id>', methods=['DELETE', 'PUT'])
def delete_update_post(id):
    # Find the book with the given ID
    post = find_post_by_id(id)

    # If the book wasn't found, return a 404 error
    if post is None:
        return f'Post with id {id} does not exist', 404

    if request.method == 'PUT':
        # Get the post data update from the client
        update_post = request.get_json()

        # if title is to be updated
        if "title" in update_post and  update_post["title"] != "":
            post["title"] = update_post["title"]

        # if content is to be updated
        if "content" in update_post and update_post["content"] != "":
            post["content"] = update_post["content"]

        return jsonify(post)
    else:
        # Remove the book from the list
        POSTS.remove(post)

        # Return the deleted book
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
