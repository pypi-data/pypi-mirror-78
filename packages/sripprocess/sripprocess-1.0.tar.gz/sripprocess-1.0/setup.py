import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sripprocess", # Replace with your own username
    version="1.0",
    author="sriram",
    author_email="shreeram7797@gmail.com",
    description="text preprocessing package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sriram7797/preprocess",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)