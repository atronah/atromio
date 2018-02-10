import os

from setuptools import setup, find_packages

README = """
atromio
=======

Getting Started
---------------

- :code:`cd atromio` - change directory into your newly created project.
- :code:`python3 -m venv env` - create a Python virtual environment.
- :code:`env/bin/activate` - activate virtual enviroment.
- :code:`env/bin/pip install --upgrade pip setuptools` - upgrade packaging tools.
- :code:`env/bin/pip install -e ".[testing]"` - install the project in editable mode with its testing requirements.
- :code:`env/bin/initialize_atromio_db development.ini` - configure the database.
- :code:`env/bin/pytest` - run your project's tests.
- :code:`env/bin/pserve development.ini` - run your project.
"""

requires = [
    'plaster_pastedeploy',
    'pyramid >= 1.9a',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='atromio',
    version='0.0',
    description='atromio',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='atronah',
    author_email='atronah.ds@gmail.com',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = atromio:main',
        ],
        'console_scripts': [
            'initialize_atromio_db = atromio.scripts.initializedb:main',
        ],
    },
)
