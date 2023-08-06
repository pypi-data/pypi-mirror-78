from setuptools import setup
import pypandoc

# with open('./README.md', encoding='utf-8') as f:
#     long_description = f.read()

# rst_description = pypandoc.convert_text(long_description, 'rst', format='markdown_github')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "relpath",
    version = '2.71',
    description = 'relative path from the python file itself',
    author = 'le latelle',
    author_email = 'g.tiger.ml@gmail.com',
    url = 'https://github.co.jp/',
    packages = ["relpath"],
    install_requires = [],
    long_description = long_description,
    long_description_content_type = "text/markdown"
)
