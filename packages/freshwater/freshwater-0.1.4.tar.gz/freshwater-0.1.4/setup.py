# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freshwater']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0']

setup_kwargs = {
    'name': 'freshwater',
    'version': '0.1.4',
    'description': 'Python module for estimating thermodynamic properties of water in freshwater lakes.',
    'long_description': 'Freshwater Toolbox \n===================\n*Compute thermodynamic properties of lake water*\n\n|Build Status|\n\nThe freshwater toolbox is a python package for estimating thermodynamic properties of water in freshwater bodies. Given temperature, salinity, and pressure, the freshwater toolbox enables the user to estimate the density, thermal expansion coefficient, specific heat capacity, speed of sound, temperature of maximum density, and freezing point of a parcel of lake water. The equation of state described in Chen and Millero (1986) [1]_ is implemented, which is suited for lake waters over the range of temperature, salinity, and pressure of 0--30 °C, 0--0.6 g/kg, and 0--180 bar, respectively.\n\nLinks\n-----\n\n-  Documentation: https://danielrobb.github.io/freshwater\n-  Source code: https://github.com/danielrobb/freshwater\n\nInstallation\n------------\n\nThe easiest way to install the freshwater toolbox is using pip::\n\n    pip install freshwater\n\nYou can also clone the source code from the `github repository <https://github.com/danielrobb/freshwater>`_ and install it with the following commands::\n\n    git clone https://github.com/danielrobb/freshwater\n    cd freshwater/\n    pip install .\n\nQuick Start\n------------\n\nSay you have a sample of lake water with temperature 10 °C, salinity 0.5 g/kg, and pressure 0 bar, and you would like to compute its density 𝜌 and thermal expansion coefficient 𝛼. This can be done with the following commands.\n\nFirst, import the equation of state (Eos) class::\n\n   >>> from freshwater.eos import Eos\n\nSecond, ``Eos`` takes arguments of temperature, salinity and pressure::\n\n   >>> e = Eos(t=10, s=0.5, p=0)\n   >>> e.rho\n   1000.091963\n   >>> e.alpha\n   8.94332e-05\n\nPlease consult the `online documentation <https://danielrobb.github.io/freshwater>`_ for more details.\n\n.. |Build Status| image:: https://travis-ci.org/danielrobb/freshwater.svg?branch=master\n   :target: https://travis-ci.org/github/danielrobb/freshwater\n   :alt: travis-ci build status\n\n.. [1] Chen, C. T. A., & Millero, F. J. (1986). Thermodynamic properties for natural waters covering only the limnological range. *Limnology and Oceanography*, 31(3), 657-662. `doi  <https://doi.org/10.4319/lo.1986.31.3.0657>`_\n\n\n',
    'author': 'danielrobb',
    'author_email': 'danielrobb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielrobb/freshwater',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
