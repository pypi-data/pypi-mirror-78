from setuptools import find_packages, setup
import semantyk

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    author = semantyk.__author__,    
    author_email = semantyk.__email__,    
    classifiers = [
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    description = 'Ideas Wonder.',    
    install_requires = ['rdflib', 'uuid'],
    keywords = 'semantyk',
    license = 'LICENSE.txt',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    maintainer = 'Semantyk',
    name = 'semantyk',
    packages = find_packages(
        exclude = {
            'docs',
            'tests*'
        }
    ),
    url = 'https://github.com/semantyk/Semantyk',
    version = semantyk.__version__
)