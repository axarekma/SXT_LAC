
from io import StringIO, BytesIO
from tarfile import TarFile
import pkgutil
import re

import numpy as np

from . import constants as CONST

def read_atomic_mass(element):
    print('Reading atomic mass for ',element)    
    find_string = f"Atomic Symbol = {element}"
    data = pkgutil.get_data(__name__, "data/NIST_atomic_weights.txt").decode()

    lines = data.split('\n')
    try:
        index = next((i, el) for i, el in enumerate(lines) if el.strip() == find_string)[0]
        return float(re.findall("\d+\.\d+", lines[index+2])[0])
    except StopIteration:
        print('Element not found!')

def absorption_cross_section(element):
    print('Reading absorption cross section for ',element)    
    nff_name = f"{element.lower()}.nff"
    data = pkgutil.get_data(__name__, f"data/sf.tar.gz")  
    with TarFile.open(fileobj=BytesIO(data)) as tf:
        x,f1,f2 =np.genfromtxt(tf.extractfile(nff_name), skip_header=1).transpose()  
    x_lambda = CONST.H*CONST.C/x
    mu_cc = 2*(CONST.RE*100)*(x_lambda*100)*f2
    return x,mu_cc

class ElementLookup():
    def __init__(self, function):
        self._data = dict()
        self._function = function

    def __call__(self, element):
        if element not in self._data:
            value = self._function(element)
            if value:
                self._data[element]=value
        return self._data[element]
   

PhotoAbsCC=ElementLookup(absorption_cross_section)
AtomicMass=ElementLookup(read_atomic_mass)

