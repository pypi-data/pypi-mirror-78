import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LbelDB",
    version="0.1.1",
    author="UnTenseUnJury",
    author_email="untenseunjury@gmail.com",
    description="A text based no corruption database for python. Easy to use. Made for beginners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UnTenseUnJury/LbelDB.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
