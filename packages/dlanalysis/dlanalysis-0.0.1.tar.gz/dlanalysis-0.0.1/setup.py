import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dlanalysis",
    version="0.0.1",
    author="Yuge Zhang",
    author_email="scottyugochang@gmail.com",
    description="Toolkit for analysis of deep learning outputs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ultmaster/dlanalysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
