Flask-Image-Search
==================

Flask-Image-Search is an extension for `Flask`_ that works with `Flask-SQLAlchemy`_ to add image searching functionally to your `Flask`_ app.
It aims to make querying your database with an image easy.

.. _Flask: http://flask.pocoo.org/
.. _Flask-SQlAlchemy: https://flask-sqlalchemy.palletsprojects.com/
.. _keras: https://keras.io/
.. _VGG16: https://keras.io/applications/#vgg16

.. module:: flask_image_search

--------
Features
--------

- Works with `Flask-SQLAlchemy`_
- Easy to use
- Small index files
- Automatically indexes new images
- And more...

------------
Installation
------------

Install Flask-Image-Search with on of these commands:

.. code-block:: text

    pip install flask_image_search

Or you can install it from github:

.. code-block:: text

    pip install git+https://github.com/hananf11/flask_image_search.git

-----
Setup
-----

Flask-Image-Search can be setup in two ways to setup the extension.
You can either initialize it directly, binding it to the application:

.. literalinclude:: ../examples/simple.py
    :lines: 5, 7-8

the alternative is for if you are using a factory pattern::

    db = SQLAlchemy()
    image_search = ImageSearch()

    def create_app():
        app = Flask(__name__)
        db.init_app(app)
        image_search.init_app(app, db)
        return app


------
Config
------

.. csv-table::
    :header: "Option", "Description", "Default"

    ``IMAGE_SEARCH_FILE_PATH_PREFIX``, This Is used to get the directory where the index files should be saved. This is combined with a Models ``__tablename__`` to get the file name and path,  ``image_search_features/``

------------
How it Works
------------

Flask-Image-Search uses `keras`_ and the `VGG16`_ Convolutional neural network for feature extraction of images.
Once all the features have been extracted from the image dataset they can be searched on. The first step is to extract the features of the query image,
then the query image features can be compared with all the other image features to get the distance between them. Flask-Image-Search does all this stuff
and turns it into a simple SQLAlchemy query.

-----
Usage
-----

Registering a Model
^^^^^^^^^^^^^^^^^^^

To register a Model you use the :meth:`ImageSearch.register()` decorator.

without a relationship
""""""""""""""""""""""

.. literalinclude:: ../examples/simple.py
    :pyobject: Image

In that example the column that stores the image path is `url`, this is the default setup.
If you want to a different column name you will need to set `url_column` to the name of your column.

with a relationship
"""""""""""""""""""

To make a Model that is related to an indexed Model image searchable, you need to track the foreign key that connects them.
you have to add the name of the foreign key to fk_cols list.

.. literalinclude:: ../examples/joined.py
    :lines: 12-23

Ignoring Images
^^^^^^^^^^^^^^^

To ignore an image you need can add a `image_search_ignore` column to your model. 
If you don't want your ignore column to be called `image_search_ignore` you can set `ignore_column` to the name of your column.

.. literalinclude:: ../examples/ignore.py 
    :lines: 11-16


Indexing a Model
^^^^^^^^^^^^^^^^

To index a model you use :meth:`ImageSearch.index_model()` you pass in the model that you want to index.

.. literalinclude:: ../examples/joined.py
    :lines: 26

If `override` is set to True then previously indexed images will be replaced.

Searching
^^^^^^^^^

With Flask-Image-Search you can search on indexed models and models that are related to an indexed model,
but the foreign key that connects them must be tracked.
See :ref:`Registering with a relationship<with a relationship>` to find out more about this.

Searching on registered model
"""""""""""""""""""""""""""""

To search on a registered model you use :meth:`ImageSearch.query_search()`,
this is a query transformer that works with :meth:`Query.with_transformation()<sqlalchemy.orm.query.Query.with_transformation()>`.

.. literalinclude:: ../examples/simple.py
    :lines: 19

To use query_search you need to pass in an image, you can either set `image_path` to the image path or set `image_data`
to a PIL :mod:`~PIL.Image`.
If `image_path` and `image_data` are both None then the query is not transformed and query_search does nothing.

To change the amount of results returned you can set the `limit` by default this is set to 20. `limit`
should be used instead of or as well as :meth:`Query.limit()<sqlalchemy.orm.query.Query.limit()>`.

If your query has more than one tables, for example ``db.session.query(Animals, Foods)`` you will need to pass in the
model that has the indexed images to the `model` parameter. Normally query_search can work out the model by itself.

Searching with join to registered model
"""""""""""""""""""""""""""""""""""""""

To search a model with a join to a related model you use :meth:`ImageSearch.query_relation_search()`,
this works very similarly to :meth:`ImageSearch.query_search()` but has more parameters.

With query_relation_search the join is done inside the function, Here is how you use it:

.. literalinclude:: ../examples/joined.py
    :lines: 30

query_relation_search takes the `image_path` and `image_data` they both work the same as with query_search.
It also has the `limit` parameter this dose not limit the number of images returned, it limits the number of models returned,
In the example above it is getting the top 5 animals because the `limit` is 5 it will return all the images connected
to these 5 animals ordered by there distance from the query image.

Just like with :ref:`query_search<Searching on registered model>` you must specify the query model if it cant be found.
But there are more parameters that may need to be set. See :meth:`~ImageSearch.query_relation_search()` to find out more.


----
Demo
----

simple example
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/simple.py

joined example
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/joined.py

---
API
---

.. autoclass:: ImageSearch
    :members:

----
More
----

.. toctree::
    licence