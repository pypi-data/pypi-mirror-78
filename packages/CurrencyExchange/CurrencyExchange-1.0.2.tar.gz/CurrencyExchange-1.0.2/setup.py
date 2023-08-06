from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='CurrencyExchange',
    version='1.0.2',
    description='A Python package that converts currencies and validates currency codes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/royshadmon/Currency-Exchange',
    author='Roy Shadmon',
    author_email='rshadmon@gmail.com',
    license='MIT',
    packages=['CurrencyExchange'],
    package_dir={'CurrencyExchange': 'src'},
    install_requires=['requests',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)