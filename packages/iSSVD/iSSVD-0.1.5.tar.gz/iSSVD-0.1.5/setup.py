import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iSSVD", 
    version="0.1.5",
    author="Weijie Zhang",
    author_email="zhan6385@umn.edu",
    description="Robust Integrative Biclustering for Multi-view Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weijie25/iSSVD",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)