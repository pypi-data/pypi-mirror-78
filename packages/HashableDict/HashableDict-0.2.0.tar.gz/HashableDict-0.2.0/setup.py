import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HashableDict",
    version="0.2.0",
    author="IFcoltransG",
    license="unlicense",
    author_email="IFcoltransG+PyPI@protonmail.ch",
    description="A hashable immutable dictionary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["dictionary", "dict", "frozen", "hashable", "immutable"],
    url="https://github.com/IFcoltransG/HashableDict",
    download_url="https://github.com/IFcoltransG/HashableDict/archive/v0.1.2.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires='>=3.7',
)
