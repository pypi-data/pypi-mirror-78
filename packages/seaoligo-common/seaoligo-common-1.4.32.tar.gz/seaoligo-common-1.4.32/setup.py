import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='seaoligo-common',
    version='1.4.32',
    author='SEA Biopharma',
    author_email='sea.biopharma@gmail.com',
    description='SEA Web Services common python packages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sea-biopharma/seaoligo-common',
    packages=setuptools.find_packages(),
    install_requires=[
        'flask>=1.1',
        'flask-sqlalchemy>=2.4',
        'graphene>=2.1',
        'pyjwt>=1.7',
    ],
    python_requires='>=3.8',
)
