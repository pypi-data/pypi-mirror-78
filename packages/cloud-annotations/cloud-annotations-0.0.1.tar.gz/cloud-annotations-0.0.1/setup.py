import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloud-annotations",
    version="0.0.1",
    author="Nick Bourdakos",
    author_email="bourdakos1@gmail.com",
    description="The Cloud Annotations python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloud-annotations/python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
