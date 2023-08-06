import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpycolors", # Replace with your own username
    version="0.0.4",
    author="ReddyyZ",
    author_email="arthurc.oli.whitehat@gmail.com",
    description="Colors on terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReddyyZ/PyColors",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)