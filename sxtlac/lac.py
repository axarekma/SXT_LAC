
import numpy as np
import re
from collections.abc import Iterable
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

        self.formula = formula
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
            float: Linear absorption coefficient in the specified unit length.
        """
        cross_sections = [abs_cc(element,energy) for element in self._elements]
        mu = (CONST.NA/self._MW)*sum([x*sigma for x,sigma in zip(self._counts,cross_sections)])
        unit_conversion = value*10**(PREFIX[unit]-PREFIX['cm'])
        return mu*self._density*unit_conversion
    

def solve_mass_fractions(composition: Iterable, molecular_weights: Iterable) -> Iterable:
    """Solve mass fraction given a molecular compositon

    Args:
        composition (Iterable): Relative composition
        molecular_weights (Iterable): Molecular weight

    Returns:
        Iterable: Mass fraction of the elements
    """
    # ensure composition is normalized
    rel_composition=np.array(composition)/np.sum(composition)
    MW = molecular_weights
    n_el = len(composition)
    M = np.matrix((n_el+1)*[MW])
    M[-1,:]=1    
    M[:n_el,:n_el] -= np.eye(n_el)*(MW/rel_composition)
    y = n_el*[0]+[1]
    x, res, rank, s = np.linalg.lstsq(M,y,rcond=None)
    return x
 


class LAC_mixture:
    def __init__(self, *args, **kwargs):
        """Calculate LAC of mixtrures of elements.
        Accepts input arguments with density either as that last argument
        or as a keyword argument.

        Elements are specified as a list of tuples where the first element is the 
        chemical composition of the elemetn and the second, the relative composition.


        """
        if 'density' in kwargs:
            density = kwargs['density']
            elements = args
        else:
            density = args[-1]
            elements = args[:-1]

        self.LACs = [LAC(el[0], density) for el in elements]
        composition = np.array([el[1] for el in elements])
        MW = [lac._MW for lac in self.LACs]
        self._mass_fraction = solve_mass_fractions(composition, MW)

    def __call__(self, energy: float, value:float = 1 , unit:str = 'um'):
        """Calculate the linear absorption coefficient for the mixture.

        Args:
            energy (float): x-ray energy [eV]
            value (float, optional): The LAC is returned in unit length of value*unit. Defaults to 1.
            unit (str, optional): The LAC is returned in unit length of value*unit. Defaults to um.

        Returns:
            float: Linear absorption coefficient for the mixture in the specified unit length.
        """
        if len(self._mass_fraction) == 0 or len(self.LACs) == 0:
            logger.error("Mass fraction or LACs list is empty.")
            return 0
        return sum([frac*element(energy,value,unit) for frac, element in zip(self._mass_fraction,self.LACs)])





