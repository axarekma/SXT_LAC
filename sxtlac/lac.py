
import numpy as np
import re

from . import constants as CONST
from .data import AtomicMass,absorption_cross_section

def gauss(x, mu, FWHM):
    sigma = FWHM/2.355
    return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x-mu)**2/(2*sigma**2))  

def integrate_energy(x, y,energy = 517, bandwidth=None, n_sigma = 5, sampling = 100):    
    if bandwidth is None:
        return np.interp(energy,x, y)
    FWHM=energy/bandwidth
    xrange = n_sigma*FWHM/2.355
    x_sample = np.linspace(energy-xrange,energy+xrange,sampling)
    y_sample = np.interp(x_sample,x, y)
    y_probe = gauss(x_sample, energy, FWHM)
    return np.sum(y_probe*y_sample)/np.sum(y_probe)

def abs_cc(element, energy, bandwidth=None):
    x,y = absorption_cross_section(element)
    return integrate_energy(x, y, energy=energy, bandwidth=bandwidth) 

def str2int(s):
    return int(s) if len(s) else 1

class LAC:
    def __init__(self, formula, density):
        self.p = re.compile("([A-Z][a-z]?)(\d*)")
        groups = self.p.findall(formula)  
        self._elements = [el[0] for el in groups]
        self._counts = [str2int(el[1]) for el in groups]
        self._MW = sum([n*AtomicMass(el) for el,n in zip(self._elements,self._counts)])
        self._density = density

    def __call__(self, energy,bandwidth = None):
        cross_sections = [abs_cc(element,energy,bandwidth) for element in self._elements]
        mu = (CONST.NA/self._MW)*sum([x*sigma for x,sigma in zip(self._counts,cross_sections)])
        return mu*self._density/10000