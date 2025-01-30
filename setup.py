from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', "r" ) as f:
    requirements = f.read().splitlines()

setup(
    name='multinetpy',
    version='0.1.2',
    packages=find_packages(),
    install_requires=requirements,
    url='',
    license="GNU License",
    author='MultineyPy',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
