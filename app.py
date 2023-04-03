from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///newsssh.db"
db.init_app(app)
import os
from werkzeug.utils import secure_filename 

UPLOAD_FOLDER ='./static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from sqlalchemy import desc


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(500), nullable = True)
    content = db.Column(db.String(10000), nullable = True)
     

    def __init__(self, title, image,content):
        self.title = title
        self.image = image
        self.content = content
         

@app.route("/add-news", methods = ['GET', 'POST'])
def addnews():
    if request.method == "GET":
        return render_template('addnews.html')
    else:
        title = request.form['title']
        img = request.files['image']
        filename = secure_filename(img.filename)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        content = request.form['content']
         
         
        new_text = News(title, filename,content)
        db.session.add(new_text)
        db.session.commit()
        return render_template('addnews.html')


@app.route("/newss")
def news():
    news = News.query.all()
    news = News.query.order_by(desc(News.id))
    next = News.query.order_by(desc(News.id)).first()
    return render_template('innovation.html', news=news , next=next)



@app.route("/newss/<int:id>/")
def new(id):
    news = News.query.get(id)
    next = News.query.order_by(desc(News.id))[:3]
    return render_template('detail.html', news=news, next=next)

 
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)