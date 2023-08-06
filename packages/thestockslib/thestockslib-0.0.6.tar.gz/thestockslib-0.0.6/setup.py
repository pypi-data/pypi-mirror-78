import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thestockslib",
    version="0.0.6",
    author="Enrico Cambiaso",
    author_email="enrico.cambiaso@gmail.com",
    description="A simple stocks package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/auino/thestockslib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
