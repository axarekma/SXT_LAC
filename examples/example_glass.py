import matplotlib.pyplot as plt
import numpy as np
from sxtlac import LAC
from sxtlac import LAC_mixture

lac_SiO2 = LAC('SiO2',2.2)
sodalime = LAC_mixture(('SiO2',74),
                       ('Na2O',13),
                       ('CaO',1.3),                   
                       2.52)

borosilicate = LAC_mixture(('SiO2',81),
                           ('B2O3',12.5),
                           ('Na2O',4),
                           ('AlO3',2.2)
                           ,2.235)

xx = np.linspace(200, 600, 100)
plt.plot(xx, 1/lac_SiO2(xx),label = 'SiO2')
plt.plot(xx, 1/sodalime(xx),label = 'SodaLime')
plt.plot(xx, 1/borosilicate(xx),label = 'Borosilicate')
plt.legend()
plt.ylabel('Attenuation length [um]')
plt.xlabel('Energy [eV]')
plt.savefig('example_mixture.png', bbox_inches = 'tight')
