import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="preeti-bhojan-core-rahem027",  # Replace with your own username
    version="0.0.1",
    author="Hemil R",
    author_email="hemilruparel2002@gmail.com",
    description="Preeti Bhojan Dore is the core of the backend for Preeti Bhojan app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/preetibhojan/backend-core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
