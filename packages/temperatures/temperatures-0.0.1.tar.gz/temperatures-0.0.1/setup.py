from setuptools import setup

setup(
    name='temperatures',
    version="0.0.1",
    description='A program that shows system temperatures in a concise string.',
    long_description=open('README.rst').read(),
    url='https://github.com/luismsgomes/temperatures',
    author='Luís Gomes',
    author_email='luismsgomes@gmail.com',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='convenience system monitor',
    install_requires=[
    ],
    package_dir={'': '.'},
    py_modules=['temperatures'],
    entry_points={
        'console_scripts': [
            'temperatures=temperatures:main',
        ],
    },
)
