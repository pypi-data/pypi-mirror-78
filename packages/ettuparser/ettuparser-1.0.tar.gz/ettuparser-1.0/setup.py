import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ettuparser", # Replace with your own username
    version="1.0",
    author="Djentelman",
    author_email="djentelman@fjandinn.ml",
    description="This package parses ETTU site for mass transit schedule.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/petruccinator3000/ETTUParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)