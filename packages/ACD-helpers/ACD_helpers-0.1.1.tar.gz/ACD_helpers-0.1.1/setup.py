import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ACD_helpers",
    version="0.1.1",
    author="Andrew Crane-Droesch",
    author_email="andrew.crane-droesch@pennmedicine.upenn.edu",
    description="Helpers; functions that I import all the time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cranedroesch/ACD_helpers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
