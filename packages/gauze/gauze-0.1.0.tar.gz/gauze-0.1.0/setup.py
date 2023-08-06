import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="gauze",
    version="0.1.0",
    description="Small library for filtering and collecting objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbowenwest/gauze",
    author="Lygon Bowen-West",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=[],
    extras_require={
        "dev": ["black", "nox", "isort", "mypy"],
        "test": ["pytest"],
    },
    project_urls={
        "Bug Reports": "https://github.com/lbowenwest/gauze/issues",
        "Source": "https://github.com/lbowenwest/gauze/",
    },
)
