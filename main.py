from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['GET', 'POST'])
def index():
    id = request.args.get("id")
    if id:
        post = Blog.query.filter_by(id=id).first()
        return render_template('post.html', title=post.title, body=post.body)

    posts = []
    count = len(Blog.query.all())
    for num in range(count, 0, -1):
        posts.append(Blog.query.filter_by(id=num).first())
    return render_template('blog.html', posts = posts)

@app.route('/newpost', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        title_error = True
        body_error = True
        if title:
            title_error = False
        if body:
            body_error = False

        if title_error or body_error:
            return render_template("newpost.html", title=title, body=body, title_error=title_error, body_error=body_error)
        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect("/blog?id={0}".format(new_post.id))
        

    return render_template("newpost.html")

if __name__ == "__main__":
    app.run()