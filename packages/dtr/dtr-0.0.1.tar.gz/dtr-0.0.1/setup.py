import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dtr",
    version="0.0.1",
    author="Marisa Kirisame",
    author_email="jerry96@cs.washington.edu",
    description="Dynamic Tensor Rematerialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uwsampl/dtr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
