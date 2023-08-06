"""
Cppyy interface for Lyncs

In this package we provide some additional tools for the usage of
[cppyy](https://cppyy.readthedocs.io/en/latest/) in the Lyncs API.
"""

__version__ = "0.0.7"

from cppyy import nullptr, cppdef, gbl
from .lib import *
from . import ll
