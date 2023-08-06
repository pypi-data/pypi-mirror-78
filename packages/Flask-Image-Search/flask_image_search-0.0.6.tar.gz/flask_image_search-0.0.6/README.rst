Flask-Image-Search
==================

Flask-Image-Search is an extension for `Flask`_ that works with `Flask-SQLAlchemy`_ to add image searching functionally to your `Flask`_ app.
It aims to make querying your database with an image easy.

.. _Flask: http://flask.pocoo.org/
.. _Flask-SQlAlchemy: https://flask-sqlalchemy.palletsprojects.com/

------------
Installation
------------

Install Flask-Image-Search with on of these commands:

.. code-block:: text

    pip install flask_image_search

Or you can install it from github:

.. code-block:: text

    pip install git+https://github.com/hananf11/flask_image_search.git

----------------
A Simple Example
----------------

.. code-block:: python

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
        animal_id = db.Column(db.ForeignKey('models.id'))

        animals = db.relationship('Animals', primaryjoin='Image.model_id == Animals.id', backref="images")


    class Animals(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.Text)


    image_search.index_model(Image)

    images = Image.query.with_transformation(image_search.query_search(image_path='query.jpg', limit=5)).all()
    print(images)
    animals = Animals.query.with_transformation(image_search.query_relation_search(image_path='query.jpg', limit=5)).all()
    print(animals)

----
Docs
----

For full documentation visit https://flask-image-search.readthedocs.io/en/latest/

-----------
Development
-----------

#. Clone the repo
    .. code-block:: text

        git clone https://github.com/hananf11/flask_image_search.git
#. move into the folder
    ``cd ./flask_image_search``
#. pip install with dev requirements
    .. code-block:: text

        pip3 install .[dev]