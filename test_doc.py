#!/usr/bin/python3
"""Testing documentation of a module
"""
from importlib import import_module
import sys

m_imported = import_module(sys.argv[1])
print(m_imported)

if m_imported.__doc__ is None:
    print("No module documentation", end=" ")
else:
    print("OK", end=" ")

functions = [func for func in dir(m_imported) if callable(getattr(m_imported, func))]
print(functions)
