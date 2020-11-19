import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="flask_blog",
    version="0.0.1",
    author="dmitriyvek",
    author_email="dmitriyvek@mail.ru",
    description="Exapmle flask blog with rest-api and jwt auth.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmitriyvek/flask_blog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.8',
)
