import setuptools
from nanoprofiler import __version__ as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nanoprofiler", # Replace with your own username
    version=version,
    author="nano",
    author_email="me@nngn.net",
    description="A small python profiler using cProfile, pstats, Pandas and matplotlib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nanogennari.gitlab.io/nanoprofiler/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib >= 3.3.1",
        "pandas >= 1.1.1",
    ],
)