import setuptools
from os import path
from io import open
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='choicepy',
    python_requires='>3.6.0',
    version='0.0.1a1',
	packages=['choicepy'],
    url='https://github.com/seyhunsaral/choicepy',
    license='MIT License',
    author='Annika Hennes, Ali Seyhun Saral',
    author_email='hennes@coll.mpg.de, saral@coll.mpg.de',
    description='A package for social choice and voting',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown', 
	install_requires=['numpy>=1.18.5'],
    zip_safe=False
)
