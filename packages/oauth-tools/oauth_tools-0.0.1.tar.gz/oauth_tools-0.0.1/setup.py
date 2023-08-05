from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['oauth_tools']
print('packages=', packages)

setup(
    name="oauth_tools",

    version="0.0.1",

    packages=packages,
    install_requires=[],
    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="An easy interface for Microsoft Office 365 Oauth Device Code authentication.",
    long_description=long_description,
    license="PSF",
    keywords="microsoft office 365 O365 Oauth Open Authentication Device Code flask grant miller",
    url="https://github.com/GrantGMiller/oauth_tools",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/oauth_tools",
    }

    # could also include long_description, download_url, classifiers, etc.
)

# to push to PyPI

# python -m setup.py sdist bdist_wheel
# twine upload dist/*