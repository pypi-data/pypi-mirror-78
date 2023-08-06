import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezbuild-pkg-CzarZappy",
    version="0.0.1",
    author="CzarZappy",
    author_email="zappy@ravenheartgames.com",
    description="A tool to help game developers build and publish their games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CzarZappy/EZBuild",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)