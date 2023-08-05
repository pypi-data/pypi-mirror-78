import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="discord_error_handle",
    version="0.0.1",
    author="Ricardolcm",
    description="A package that converts all things in a list into either string or int",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Ricardolcm888/discord_error_handle",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)