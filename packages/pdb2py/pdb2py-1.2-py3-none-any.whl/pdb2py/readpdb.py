#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:38:22 2020

@author: guterlj
"""

#pip install idlmagic
#FileName='test.pdb'
#spec = IDL.file_import(FileName)
import pidly,os,shutil
try:
    PackageDirectory = os.path.dirname(os.path.abspath(__file__))
except:
    PackageDirectory=os.getcwd()

def ReadPDBFile(FileName,PathPDBLib=None,Verbose=False):
    """Read a pdb file and return a dictionary with content of the file.
    
    Note: This package comes with a pre-compiled dynalic library pdb2idl.so
    If you wish to use your own dynamic library, you must provide a path toward pdb2idl.so:
    >>> ReadPDBFILE('path/to/File',PathPDBLib=/path/to/pdb2idl.so')
    """
    PathIDLLib=os.path.join(PackageDirectory,'libIDL')
    if PathPDBLib is not None:
        shutil.copy(PathPDBLib, PathIDLLib)
    
    if Verbose:
        print('PathIDLLib:',PathIDLLib)
        #print('PathPDBLib:',PathPDBLib)
    
    StrPathIDLLib="!path = !path+':'+expand_path('{}')".format(PathIDLLib)
    idlexec=shutil.which('idl')
    
    
    CWD=os.getcwd()
    os.chdir(PathIDLLib)

    idl = pidly.IDL(idlexec)
    idl.ex(StrPathIDLLib)
    idl.pro('.r pdb2idl')
    os.chdir(PathIDLLib)
    Out=idl.func('file_import',FileName)
    os.chdir(CWD)
    return Out