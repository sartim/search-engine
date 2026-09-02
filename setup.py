from pathlib import Path

from setuptools import find_packages, setup

root = Path(__file__).parent
long_description = (root / "README.md").read_text(encoding="utf-8")

setup(
    name="search-engine",
    version="1.1.0",
    description="Semantic search helpers backed by Elasticsearch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sartim/search-engine",
    author="sartim",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "certifi>=2023.7.22",
        "elasticsearch>=8.10,<9",
        "sentence-transformers>=2.2,<4",
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
