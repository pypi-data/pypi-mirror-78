import setuptools

__VERSION__ = '1.0.1'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='AX3 Mixins',
    version=__VERSION__,
    author='Axiacore',
    author_email='info@axiacore.com',
    description='Mixins for use into the AX3 tech stack',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/axiacore/ax3-mixins',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
