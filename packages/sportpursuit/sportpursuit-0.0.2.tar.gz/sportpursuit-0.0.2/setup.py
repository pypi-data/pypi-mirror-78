import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sportpursuit", 
    version="0.0.2",
    author="georgebiggs",
    author_email="george.biggs@sportpursuit.com",
    description="A package containing key sp functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/georgebiggs/sp_py_pkg",
    test_suite="tests",
    # packages=setuptools.find_packages(),
    install_requires=["pandas","psycopg2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)