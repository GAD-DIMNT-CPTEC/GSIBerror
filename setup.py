from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).parent

setup(
    name="GSIBerror",
    version="1.1.0",
    author="Carlos Frederico Bastarz",
    author_email="carlos.bastarz@inpe.br",
    url="https://github.com/GAD-DIMNT-CPTEC/GSIBerror",
    project_urls={
        "Documentation": "https://gad-dimnt-cptec.github.io/GSIBerror",
    },
    license="CC BY-NC-SA-4.0",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    description="A Python class to read the records and attributes from the background error covariance matrices compatible with the Gridpoint Statistical Interpolation in the .gcv file format.",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.22",
        "xarray",
        "Cartopy>=0.22.0",
        "matplotlib",
    ],
    extras_require={"dev": ["pytest>=7", "ruff", "twine>=4.0.2"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9.18",
)
