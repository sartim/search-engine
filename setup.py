from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="search-engine",
    version="1.0.0",
    description="Search Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sartim/search-engine",
    author='@sartim',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "elasticsearch",
        "scikit-learn",
        "sentence-transformers",
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
