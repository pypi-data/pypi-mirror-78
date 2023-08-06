import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Vys",
    version="0.2.1",
    author="Connor White",
    author_email="connorwhite101@gmail.com",
    description="A collection of classes that allow for easier usage of common packages. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.connorwhite.uk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'openpyxl',
        'mysql-connector-python',
        'python-dateutil'
    ],
    python_requires='>=3.6',
)
