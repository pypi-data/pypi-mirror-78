import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="PyBlox2",
    version="v1.0.0-beta",
    author="Kyando",
    author_email="amehikoji@gmail.com",
    description="Handler for the Roblox API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kyando2/PyBlox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)