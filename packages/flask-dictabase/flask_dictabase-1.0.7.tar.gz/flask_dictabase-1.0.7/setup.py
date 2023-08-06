from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['flask_dictabase']

setup(
    name="flask_dictabase",

    version="1.0.7",
    # 1.0.7 - Added BaseTable Set/Get methods to help deal with unsuported db types

    packages=packages,
    install_requires=[
        'flask',
        'dataset',
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A dict() like interface to your database.",
    long_description=long_description,
    license="PSF",
    keywords="grant miller flask database",
    url="https://github.com/GrantGMiller/flask_dictabase",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/flask_dictabase",
    }

)
