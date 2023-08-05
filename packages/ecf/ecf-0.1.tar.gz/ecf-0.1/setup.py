import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecf",
    version="0.1",
    author="Pierre-François Gimenez",
    author_email="<pierre-francois.gimenez@laas.fr>",
    description="Empirical Christoffel function for outlier detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PFGimenez/ecf-outlier-detection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
