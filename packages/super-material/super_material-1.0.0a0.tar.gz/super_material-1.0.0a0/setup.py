# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['super_material',
 'super_material.conductivity',
 'super_material.gap_energy',
 'super_material.integrate']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'super-material',
    'version': '1.0.0a0',
    'description': 'Providing a constant interface to superconductor conductivity computations',
    'long_description': '# Super Material\n\nProviding a constant interface to superconductor conductivity computations.\n\n## Motivation\n\nA lot of superconductor electromagnetic simulations can be transformed into classical computational electromagnetic (CEM) problems by substituting a complex conductivity term. Calculating these superconductor conductivity terms can be trivial, such as when calculating the two-fluid superconductor conductivity, but can also be numerically challenging, such as when calculating the Zimmermann superconductor conductivity. Calculating the superconductor conductivity term oneself does not give someone trying to solve a classical electromagnetic problem any advantage. With this library, one can directly jump into the CEM problem rather than spending time evaluating superconductor conductivity terms.\n\nOther codes for calculating these terms are available, but some are numerically unstable and inefficient. We aim to provide a range of efficient and numerically stable set of routines.\n\n## Installation\n\nGeneral users should install the latest release with pip\n\n```bash\npip install super_material\n```\n\nDevelopers should install from the source directory using poetry\n\n```bash\npoetry install\n```\n\n## Usage example\n\nA simple example showing how to calculate the Mattis-Bardeen superconductor conductivity for Niobium at 4.2 K and 100 GHz.\n\n```python\nfrom super_material import BCSGapEnergy, MattisBardeenSuperconductorConductivity\n\nconductivity_0 = 2.4e7 # in Siemens per meter\ntemperature = 4.2 # in K\ngap_energy_0 = 1.5e-3 # in eV\nfrequency = 100e9 # in Hz\nkappa = 4000\n\ngap_energy = BCSGapEnergy(gap_energy_0, 4000)\nconductivity = MattisBardeenSuperconductorConductivity(gap_energy, conductivity_0)\nresult = conductivity.evaluate(temperature, frequency)\nprint(f"sigma = {result}")\n```\n\nFor more information see the [full documentation](https://pleroux0.github.io/super_material/)\n\n## Acknowledgements\n\nThis project was developed under IARPA contract SuperTools\n(via the U.S. Army Research Office grant W911NF-17-1-0120).\n\n## License\n\nThis project is licensed under the 2-Clause BSD license for maximum usability.\n\nSee [LICENSE.md](LICENSE.md) for more information\n',
    'author': 'Paul le Roux',
    'author_email': 'pleroux0@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pleroux0/super_material',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
