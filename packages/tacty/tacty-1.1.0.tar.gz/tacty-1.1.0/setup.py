import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tacty",  # Replace with your own username
    version="1.1.0",
    author="Cristian Gonzalez",
    author_email="cristian.gsp@gmail.com",
    description="An extensible command bus for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cristiangsp/tacty",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
