import setuptools
import io
import re

#with open("./README.md", "r") as fh:
#    long_description = fh.read()
with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()
setuptools.setup(
    name="sivapackage",
    version="0.0.1",
    author="krishna",
    author_email="cloud@cloudstones.org",
    description="my description",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://cloudstones.org",
    py_modules=["krishnacalci"],
    package_dir={'': 'src'},
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
