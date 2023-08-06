import sys

from lyncs_setuptools import setup, CMakeExtension
from lyncs_clime import __path__ as lime_path

setup(
    "lyncs_tmLQCD",
    data_files=[(".", ["config.py.in"])],
    ext_modules=[
        CMakeExtension(
            "lyncs_tmLQCD.lib",
            ".",
            [
                "-DLIME_PATH=%s" % lime_path[0],
            ],
        )
    ],
    install_requires=[
        "lyncs-cppyy",
        "lyncs-clime",
        "numpy",
    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
    },
    keywords=[
        "Lyncs",
        "tmLQCD",
        "Lattice QCD",
        "Wilson",
        "Twisted-mass",
        "Clover",
        "Fermions",
        "HMC",
        "Actions",
        "ETMC",
    ],
)
