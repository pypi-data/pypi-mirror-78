import setuptools


import cliagramme


with open("README.md", "r") as fichier:
    long_description = fichier.read()


setuptools.setup(
    name = "cliagramme",
    version = cliagramme.__version__,
    author = "Asurix",
    author_email = "asurix@outlook.fr",
    description = "Afficher et gérer des diagrammes en console.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/4surix/cliagramme",
    packages = setuptools.find_packages(),
    keywords = 'diagramme cli console shell',
    plateformes = 'ALL',
    install_requires = ['colorama>=0.4.3'],
    classifiers = [
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires = '>=3.6, <4',
)