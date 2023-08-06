from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Summer-Project',
    version='v2.0',
    packages=['Stock_Analysis'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ARU300',
    author_email='ath.projalph@gmail.com',
    description='Summer Project',
    url='https://github.com/ARU300/SummerProject/archive/2.0.zip',
    keywords=['Machine Learning', 'Python3'],
    classifiers=[],
)