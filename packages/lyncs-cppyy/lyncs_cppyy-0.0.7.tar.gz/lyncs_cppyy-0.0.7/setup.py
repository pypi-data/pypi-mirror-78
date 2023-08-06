import glob
from lyncs_setuptools import setup

setup(
    "lyncs_cppyy",
    install_requires=["cppyy>=1.8.1", "numpy"],
    keywords=[
        "Lyncs",
        "cppyy",
    ],
    extras_require={
        "test": ["pytest", "pytest-cov", "meson", "ninja"],
    },
    data_files=[("test/cnumbers", glob.glob("test/cnumbers/*"))],
)
