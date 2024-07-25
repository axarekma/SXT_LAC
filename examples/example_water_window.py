import matplotlib.pyplot as plt
import numpy as np
from sxtlac import LAC

xx = np.linspace(200, 600, 100)
lac_H2O = LAC('H2O',1)(xx)
lac_SiO2 = LAC('SiO2',2.2)(xx)
lac_C = LAC('C',2.2)(xx)
plt.plot(xx,1/lac_H2O,label = 'H2O')
plt.plot(xx,1/lac_SiO2,label = 'SiO2')
plt.plot(xx,1/lac_C,label = 'C')
plt.legend()
plt.ylabel('Attenuation length [um]')
plt.xlabel('Energy [eV]')
plt.savefig('example.png', bbox_inches = 'tight')