from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

DATA_FILE = "data/blog_db.json"

def load_posts():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=2, ensure_ascii=False)

def fetch_post_by_id(blog_posts, post_id):
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        if not author or not title or not content:
            return "All fields are required", 400

        new_post = {
            "id": max([post["id"] for post in blog_posts], default=0) + 1,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()
    post = fetch_post_by_id(blog_posts, post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post["author"] = request.form.get('author')
        post["title"] = request.form.get('title')
        post["content"] = request.form.get('content')

        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()

    filtered_posts = [
        post for post in blog_posts
        if post["id"] != post_id
    ]

    if len(filtered_posts) == len(blog_posts):
        return "Post not found", 404

    save_posts(filtered_posts)

    return redirect(url_for('index'))

@app.route('/like/<int:post_id>')
def like(post_id):
    blog_posts = load_posts()
    post = fetch_post_by_id(blog_posts, post_id)

    if post is None:
        return "Post not found", 404

    post["likes"] += 1

    save_posts(blog_posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
