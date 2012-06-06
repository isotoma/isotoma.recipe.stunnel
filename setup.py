from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name = 'isotoma.recipe.stunnel',
    version = version,
    description = "Buildout recipes to configure the stunnel SSL terminator",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    url = "http://pypi.python.org/pypi/isotoma.recipe.stunnel",
    classifiers = [
        "Framework :: Buildout",
        "Framework :: Buildout :: Recipe",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords = "proxy ssl stunnel buildout",
    author = "John Carr",
    author_email = "john.carr@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
        'isotoma.recipe.stunnel.templates': ['stunnel.conf.j2']
    },
    namespace_packages = ['isotoma', 'isotoma.recipe'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'zc.buildout',
        'Jinja2',
        'isotoma.recipe.gocaptain',
        'missingbits',
    ],
    entry_points = {
        "zc.buildout": [
            "default = isotoma.recipe.stunnel:Stunnel",
        ],
    }
)
