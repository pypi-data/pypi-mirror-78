import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', "r") as fh:
    requirements = fh.read().split("\n")

print("requirements: ", requirements)

print("setuptools.find_packages(): ", setuptools.find_packages())

from transpy import __version__

setuptools.setup(
    name="transpy",
    version=__version__,
    author="",
    author_email="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coderepocenter/TransPy.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)