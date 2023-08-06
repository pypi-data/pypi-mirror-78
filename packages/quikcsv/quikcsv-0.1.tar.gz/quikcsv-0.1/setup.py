import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='quikcsv',
    version='0.1',
    author='Bryn Mck',
    description='Decorator for making quick mock csv files for testing.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PRIV00/quikcsv',
    packages=setuptools.find_packages(),
    python_required='>=3.8'
)
