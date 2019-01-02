import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neohub",
    version="0.2.0",
    author="Vlatko Kosturjak",
    author_email="vlatko.kosturjak@gmail.com",
    description="Control Neohub supported thermostats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kost/neohub-python",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
	"Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

