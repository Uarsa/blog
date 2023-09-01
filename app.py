from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(20))
    type = db.Column(db.String(10))
    device = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    part_price = db.Column(db.Integer())
    total_price = db.Column(db.Integer())
    income = db.Column(db.Integer)

    def __repr__(self):
        return '<Article %r>' % self.id


'''
@app.route('/')
@app.route('/home')
def index():
    #first way was:
    #return render_template('index.html')
    #then this:
    arts = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', arts=arts)
'''


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def posts():
    # get first element from table
    # articles = Article.query.first()
    # get all elements
    # articles = Article.query.all()
    # get all elements sorted by column

    if request.method == "POST":
        find = request.form['find']
        find = find.lower()
    
        articles = Article.query.order_by(Article.date.desc()).all()

        texts = []
        for el in articles:
            s = "{} {} {} {} {} {} {} {}".format(el.name, el.tel, el.type, el.device, el.description, el.part_price, el.total_price, el.income).lower()
            texts.append(s)
    
        matches = []
        for row in texts:
            if find in row:
                matches.append(texts.index(row))
        
        arts = []
        for index in matches:
            arts.append(articles[index])
        
        return render_template('posts.html', arts=arts)
    
    else:
        
        arts = Article.query.order_by(Article.date.desc()).all()
        return render_template('posts.html', arts=arts)


'''
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
        find = find.lower()
    
        articles = Article.query.order_by(Article.date.desc()).all()
     
        texts = []
        for el in articles:
            s = "{} {} {} {}".format(el.name, el.tel, el.device, el.description).lower()
            texts.append(s)
    
        matches = []
        for row in texts:
            if find in row:
                matches.append(texts.index(row))
        
        arts = []
        for index in matches:
            arts.append(articles[index])
        
        return render_template('find.html', arts=arts)
    
    else:
        return render_template('find.html')
#test area
'''


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
        return redirect('/')
    except:
        return "Error. Post not delete..."


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        name = request.form['name']
        tel = request.form['tel']
        type = request.form['type']
        device = request.form['device']
        description = request.form['description']
        part_price = request.form['part_price']
        total_price = request.form['total_price']
        income = int(total_price) - int(part_price)
        # print(type(part_price))
        # print(type(total_price))

        article = Article(name=name,
                          tel=tel,
                          type=type,
                          device=device,
                          description=description,
                          part_price=part_price,
                          total_price=total_price,
                          income=income
                          )

        db.session.add(article)
        db.session.commit()
        return redirect('/')

        # except: return "There was an error adding the article..."

    else:
        return render_template('create_article.html')


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.name = request.form['name']
        article.tel = request.form['tel']
        article.type = request.form['type']
        article.device = request.form['device']
        article.description = request.form['description']
        article.part_price = request.form['part_price']
        article.total_price = request.form['total_price']
        # article.total_price = request.form['income']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "An error occurred while editing the article..."

    else:
        return render_template('post_update.html', article=article)


'''
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f"User: {name}, id: {id}."
'''


if __name__ == '__main__':
    app.run(debug=True)


