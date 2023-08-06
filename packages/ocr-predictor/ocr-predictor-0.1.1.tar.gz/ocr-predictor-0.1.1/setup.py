import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocr-predictor",
    version="0.1.1",
    author="pbcquoc",
    author_email="pbcquoc@gmail.com",
    description="common predictors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbcquoc/predictor",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
