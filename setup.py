import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="flask_blog",
    version="0.0.1",
    author="dmitriyvek",
    author_email="dmitriyvek@example.com",
    description="A small description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmitriyvek/flask_blog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
