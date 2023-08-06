import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strlistsmanipulator", # Replace with your own username
    version="0.0.2",
    author="Anna Fabris",
    author_email="anna.fabris@studio.unibo.com",
    description="A package to modify lists of string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/AnnaFabris/string-list-manipulator",
    install_requires=['xlsxwriter'],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
