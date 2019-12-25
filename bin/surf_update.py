#! /usr/bin/env python2.7

import os, os.path as op
import sys
import numpy as np

TRIANGLE_MAGIC = 16777214
QUAD_MAGIC = 16777215
NEW_QUAD_MAGIC = 16777213

def _fread3(fobj):
    """Read a 3-byte int from an open binary file object

    Parameters
    ----------
    fobj : file
        File descriptor

    Returns
    -------
    n : int
        A 3 byte int
    """
    b1, b2, b3 = np.fromfile(fobj, ">u1", 3)
    return (b1 << 16) + (b2 << 8) + b3

if __name__ == "__main__":
    filename = sys.argv[1]

    oldfl = open(filename,'rb')
    magic = _fread3(oldfl)
    oldfl.seek(0)
    if magic not in [TRIANGLE_MAGIC, QUAD_MAGIC, NEW_QUAD_MAGIC]:
        os.sys.exit(0) 
    lines = oldfl.readlines()
    oldfl.close()

    newfl = open(filename,'wb')
    if (len(lines)>1) and (len(lines[1])>0):
        lines.insert(1,b'\n')
    else:
        exit(0)
    newfl.writelines(lines)
    newfl.close()
