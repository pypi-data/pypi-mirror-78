import setuptools
from readme_renderer import rst

README = open('README.md').read()

setuptools.setup(
    name='adfly-api',
    version='1.0.2',
    url='https://github.com/modbender/adfly-api',
    description='Unofficial Adfly API wrapper',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Yashas H R',
    author_email='rameshmamathayashas@gmail.com',
    install_requires=[
        'httplib2',
    ],
    python_requires='>=3.5',
    platforms=['any'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
