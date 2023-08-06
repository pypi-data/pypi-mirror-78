import setuptools


import atomion


with open("README.md", "r", encoding='utf-8') as fichier:
    long_description = fichier.read()


setuptools.setup(
    name = "atomion",
    version = atomion.__version__,
    author = "Asurix",
    author_email = "asurix@outlook.fr",
    description = "Manipuler des atomes, ions et molécule facilement.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/4surix/atomion",
    packages = setuptools.find_packages(),
    keywords = 'atome ion molecule',
    classifiers = [
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires = '>=3.6, <4',
)