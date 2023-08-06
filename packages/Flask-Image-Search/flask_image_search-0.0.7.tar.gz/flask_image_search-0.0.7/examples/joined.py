from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_image_search import ImageSearch

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

image_search = ImageSearch(app, db)


@image_search.register(fk_cols=['animal_id'])
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    animal_id = db.Column(db.ForeignKey('animals.id'))

    animal = db.relationship('Animals', primaryjoin='Image.animal_id == Animals.id', backref="images")


class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


image_search.index_model(Image)

images = Image.query.with_transformation(image_search.query_search(image_path='query.jpg', limit=5)).all()
print(images)
animals = Animals.query.with_transformation(image_search.query_relation_search(image_path='query.jpg', limit=5)).all()
print(animals)
