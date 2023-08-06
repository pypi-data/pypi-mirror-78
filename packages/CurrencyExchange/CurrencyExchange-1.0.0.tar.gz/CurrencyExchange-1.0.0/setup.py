from setuptools import setup

setup(
    name='CurrencyExchange',
    version='1.0.0',
    description='A Python package that converts currencies.',
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