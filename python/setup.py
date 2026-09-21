from setuptools import find_packages
from setuptools import setup

import os

# PJ13 packaging (2026-09): upper bounds = latest version verified to install and
# reproduce the 2021 snapshot (see test/pj13_diff/); pandas<2.1 is forced by scprep 1.2.3,
# numpy<2 because pandas 2.0.x wheels are built against numpy 1.x.
install_requires = [
    "numpy>=1.14.0,<1.27",
    "scipy>=1.1.0,<1.18",
    "matplotlib<3.12",
    "scikit-learn>=0.19.1,<1.10",
    "future<2",
    "tasklogger>=1.0.0,<2",
    "graphtools>=1.4.0,<3",
    "pandas>=0.25,<2.1",
    "scprep>=1.0,<2",
]

test_requires = ["nose2", "anndata", "coverage", "coveralls"]

doc_requires = [
    "sphinx",
    "sphinxcontrib-napoleon",
]

version_py = os.path.join(os.path.dirname(__file__), "magic", "version.py")
version = open(version_py).read().strip().split("=")[-1].replace('"', "").strip()

readme = open("README.rst").read()

setup(
    name="magic-impute",
    version=version,
    description="MAGIC",
    author="",
    author_email="",
    packages=find_packages(),
    license="GNU General Public License Version 2",
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"test": test_requires, "doc": doc_requires},
    test_suite="nose2.collector.collector",
    long_description=readme,
    url="https://github.com/KrishnaswamyLab/MAGIC",
    download_url="https://github.com/KrishnaswamyLab/MAGIC/archive/v{}.tar.gz".format(
        version
    ),
    keywords=[
        "visualization",
        "big-data",
        "dimensionality-reduction",
        "embedding",
        "manifold-learning",
        "computational-biology",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
