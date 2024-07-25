
import numpy as np
import re
from collections.abc import Iterable

from .constants import PREFIX
from . import constants as CONST

from .data import AtomicMass,PhotoAbsCC

def abs_cc(element, energy):
    x,y = PhotoAbsCC(element)
    return np.interp(energy,x, y)

def str2int(s):
    return int(s) if len(s) else 1

class LAC:
    def __init__(self, formula : str, density : float):
        """Lookup for the linear absorption coefficient of compound elements.

        Args:
            formula (str): Chemical Formula: Note that this is case sensitive. 
            density (float): Material density in units of gm/cm^3.
        """

        groups = re.compile("([A-Z][a-z]?)(\d*)").findall(formula)  
        self._elements = [el[0] for el in groups]
        self._counts = [str2int(el[1]) for el in groups]
        self._MW = sum([n*AtomicMass(el) for el,n in zip(self._elements,self._counts)])
        self._density = density

    def __call__(self, energy: float, value:float = 1 , unit:str = 'um'):
        """Retrieve the LAC. The LAC is retruned in the length scale of 
            [L] = value unit        

        Args:
            energy (float): x-ray energy [eV]
            value (float, optional): The LAC is returned in unit length of value*unit. Defaults to 1.
            unit (str, optional): The LAC is returned in unit length of value*unit. Defaults to um.

        Returns:
            _type_: _description_
        """
        cross_sections = [abs_cc(element,energy) for element in self._elements]
        mu = (CONST.NA/self._MW)*sum([x*sigma for x,sigma in zip(self._counts,cross_sections)])
        unit_conversion = value*10**(PREFIX[unit]-PREFIX['cm'])
        return mu*self._density*unit_conversion