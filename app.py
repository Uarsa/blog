from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(20))
    device = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    #first way was:
    #return render_template('index.html')
    #then this:
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    # get first element from table
    # articles = Article.query.first()
    # get all elements
    # articles = Article.query.all()
    # get all elements sorted by column
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


#test area
@app.route('/find', methods=['POST', 'GET'])
#@app.route('/find')
def find():
    # get first element from table
    # articles = Article.query.first()
    # get all elements
    # articles = Article.query.all()
    # get all elements sorted by column
    
    if request.method == "POST":
        find = request.form['find']
    
        articles = Article.query.order_by(Article.date.desc()).all()

        texts = []
        for el in reversed(articles):
            s = "{} {} {} {}".format(el.name, el.tel, el.device, el.description)
            texts.append(s)
    
        matches = []
        for row in reversed(texts):
            if find in row:
                matches.append(texts.index(row)+1)

        return render_template('find.html', matches=matches, articles=articles)
    
    else:
        return render_template('find.html')
#test area


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error. Post not delete..."


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        name = request.form['name']
        tel = request.form['tel']
        device = request.form['device']
        description = request.form['description']

        article = Article(name=name,
                          tel=tel,
                          device=device,
                          description=description
                          )

        db.session.add(article)
        db.session.commit()
        return redirect('/posts')

        # except: return "There was an error adding the article..."

    else:
        return render_template('create_article.html')


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.name = request.form['name']
        article.tel = request.form['tel']
        article.device = request.form['device']
        article.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while editing the article..."

    else:
        return render_template('post_update.html', article=article)


'''
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f"User: {name}, id: {id}."
'''

# test Git...

if __name__ == '__main__':
    app.run(debug=True)



