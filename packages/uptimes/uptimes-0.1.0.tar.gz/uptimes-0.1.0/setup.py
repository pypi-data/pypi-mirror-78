import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="uptimes",
    version="0.1.0",
    author="Tim232",
    author_email="endbot4023@gmail.com",
    description="A small python3 package for uptimes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tim232/uptimes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)