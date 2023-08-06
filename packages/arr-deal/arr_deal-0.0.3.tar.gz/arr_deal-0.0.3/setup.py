import setuptools
with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arr_deal",
    version="0.0.3",
    author="Shubham Rajak",
    description="Just a small effort",
    long_description=long_description,
    long_description_content_typt="text/markdown",
    url="https://github.com/urplatshubham/arr_deal",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
