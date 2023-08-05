import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chosungify", 
    version="0.0.1",
    author="Joon-Won Choi",
    author_email="requiemdeciel@gmail.com",
    description="Small snippet for extracting korean consonant character.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SHUcream00/chosungify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)