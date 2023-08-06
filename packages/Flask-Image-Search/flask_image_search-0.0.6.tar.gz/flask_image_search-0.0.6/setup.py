import io
import re

from setuptools import setup

with io.open("flask_image_search/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read(), re.M).group(1)

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='flask_image_search',
    version=version,
    description="Flask Image Search works with Flask-SQLAlchemy to add image searching functionality",
    packages=["flask_image_search"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Topic :: Database"
    ],
    long_description=long_description,
    install_requires=[
        "Flask>=1.1.1",
        "Flask_SQLAlchemy>=2.4.1",
        "Keras>=2.3.1",
        "numpy>=1.18.1",
        "pillow>=7.1.1",
        "tensorflow>=2.1.0"
    ],
    extras_require={
        "dev": [
            "twine==3.1.1",
            "sphinx==3.0.2",
            "Pallets_Sphinx_Themes==1.2.3",
            "check_manifest"
        ]
    },
    url="https://github.com/hananf11/flask_image_search",
    project_urls={
        "Documentation": "https://flask-image-search.readthedocs.io/",
        "Issues": "https://github.com/hananf11/flask_image_search/issues"
    },
    author="Hanan Fokkens",
    author_email="hananfokkens@gmail.com"
)
