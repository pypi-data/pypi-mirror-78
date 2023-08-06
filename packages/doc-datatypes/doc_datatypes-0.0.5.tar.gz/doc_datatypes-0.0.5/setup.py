import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doc_datatypes",
    version="0.0.5",
    author="Example Author",
    author_email="rickeyfsimple@example.com",
    description="Data types with documentation _-_",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kel0/doc_dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7',
)