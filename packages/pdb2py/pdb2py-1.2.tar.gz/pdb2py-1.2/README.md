pdb2py
======
Python package to read a pdb file into a python dictionary.

Usage:
>>> from pdb2py import *
>>> Data=ReadPDBFile('path/to/a/PDB/file')

Note: 
    This package comes with a pre-compiled dynalic library pdb2idl.so
    If you wish to use your own dynamic library, you must provide a path toward pdb2idl.so:
    >>> ReadPDBFILE('path/to/File',PathPDBLib=/path/to/pdb2idl.so')
    
Author: J. Guterl at General Atomics (guterlj@fusion.gat.com) 
August 2020
 