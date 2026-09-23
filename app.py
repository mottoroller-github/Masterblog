from flask import Flask, render_template
import json
app = Flask(__name__)

DATA_FILE = "data/blog_db.json"

def load_posts():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
