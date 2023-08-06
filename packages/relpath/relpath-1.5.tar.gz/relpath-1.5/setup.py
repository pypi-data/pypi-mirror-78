from setuptools import setup

setup(
    name = "relpath",
    version = '1.5',
    description = 'relative path from the python file itself',
    author = 'le latelle',
    author_email = 'g.tiger.ml@gmail.com',
    url = 'https://github.co.jp/',
    packages = ["relpath"],
    install_requires = [
    	"pathlib==1.0.1",
    ]
)
