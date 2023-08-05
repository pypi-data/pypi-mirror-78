import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="krishnapack",
    version="0.0.1",
    author="krishna",
    author_email="cloud@cloudstones.org",
    description="my description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cloudstones.org",
    py_modules=["krishnacalci"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
