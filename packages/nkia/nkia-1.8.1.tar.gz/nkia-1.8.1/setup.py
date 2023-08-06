import os
from pathlib import Path
from setuptools import setup
import json
from src.utils.utils import read_file

long_description = read_file(os.getcwd() + '/README.md')
version = json.loads(read_file(os.getcwd() + '/config.txt'))

setup(
    name='nkia',
    version=version['version'],
    description='This is a module to predict the products category using artificial inteligence.',
    url='https://bitbucket.org/nksistemasdeinformacao/servicos-biodigital/src/master/',
    download_url='https://bitbucket.org/nksistemasdeinformacao/servicos-biodigital/src/master/',
    license='Apache License 2.0',
    author='NK Sistemas de Informacao em Saude',
    author_email='ti@nkodontologia.com.br',

    py_modules=['nkia/ml/classify_products', 'nkia/ml/cnn_nlp_model', 'utils/utils'],
    
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['tensorflow', 'nlp', 'nk',
              'python3', 'cnn', 'food-products'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    python_requires='>=3.6',
    install_requires=[
        'tensorflow==2.2.0',
        'numpy==1.19.1',
        'tensorflow-datasets==3.2.1',
        'Unidecode==1.1.1',
        'nltk==3.5',
        'gdown==3.12.0',
        'scikit-learn==0.23.2',
        'pandas==0.23.4',
        'symspellpy==6.5.2'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7'
        ]
    }
)