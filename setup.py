from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flk',
    version='1.2.3',
    description='FLK - это библиотека для парсинга и работы с файлами в формате FL (File Language).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='FlacSy',
    author_email='flacsy.tw@gmail.com',
    packages=find_packages(),
    url='https://github.com/FlacSy/flk',
)