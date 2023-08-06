import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dicemaths",
    version="0.2.0",
    author="AlDacMac",
    author_email="alasdairmacgdev@gmail.com",
    description="Package for performing basic statistical calculations on the outcomes of dice rolls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlDacMac/dicemaths",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)