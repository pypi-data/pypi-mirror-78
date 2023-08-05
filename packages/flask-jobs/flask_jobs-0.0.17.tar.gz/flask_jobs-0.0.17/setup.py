from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['flask_jobs']
print('packages=', packages)

setup(
    name="flask_jobs",

    version="0.0.17",

    packages=packages,
    install_requires=['flask_dictabase'],

    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="An easy job scheduling interface for flask projects.",
    long_description=long_description,
    license="PSF",
    keywords="flask job scheduler apscheduler celery redis",
    url="https://github.com/GrantGMiller/flask_jobs",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/flask_jobs",
    }
)

# to push to PyPI

# test postgres: 'postgres://xfgkxpzruxledr:5b83aece4fbad7827cb1d9df48bf5b9c9ad2b33538662308a9ef1d8701bfda4b@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d8832su8tgbh82'
# python -m setup.py sdist bdist_wheel
# twine upload dist/*