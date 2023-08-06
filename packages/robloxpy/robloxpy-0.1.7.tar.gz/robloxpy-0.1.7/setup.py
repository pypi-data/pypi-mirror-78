#from setuptools import setup
import setuptools
with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='robloxpy',
    version='0.1.7',
    author="Kristan Smout",
    author_email="python@kristansmout.com",
    description="Wrapper for roblox Web API's",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KristanSmout/RobloxPyOfficial",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Attribution Assurance License",
        "Operating System :: OS Independent",
    ],
)
    