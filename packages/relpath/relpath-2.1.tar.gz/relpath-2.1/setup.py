from setuptools import setup

with open('./README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "relpath",
    version = '2.1',
    description = 'relative path from the python file itself',
    author = 'le latelle',
    author_email = 'g.tiger.ml@gmail.com',
    url = 'https://github.co.jp/',
    packages = ["relpath"],
    install_requires = [
    ],
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)
