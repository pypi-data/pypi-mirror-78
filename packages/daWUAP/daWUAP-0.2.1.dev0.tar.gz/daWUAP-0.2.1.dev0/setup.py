from setuptools import find_packages
# from Cython.Build import cythonize

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = '''
The data assimilation Water Use and Agricultural Productivity model (daWUAP) is a hydro-economic model that couples an economic model of agricultural production calibrated using positive mathematical programming (PMP) and a semidistributed rainfall-runoff-routing model that simulates water available to producers.

Features:

- Calibration of economic component can use standard the mathematical programming method or a new recursive stochastic filter.
- Stochastic calibration permits to obtain simulation results of agricultural outputs (land and water allocation, etc) as probability distributions that reflect the quality of the calibration.
- Recursive stochastic filter permits calibration of economic model with noisy but frequent remote sensing observations of agricultural activity.
- Model permits to trace the effect of producer choices on the hydrologic system and on other users.

[Contributions and comments are welcome at Github.](https://bitbucket.org/umthydromodeling/dawuap.git)
'''

config = {
    'name': 'daWUAP',
    'version': '0.2.1.dev',
    'author': 'Marco Maneta',
    'author_email': 'marco.maneta@umontana.edu',
    'description': 'Hydrologic Engine for daWUAP model',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'url': 'https://bitbucket.org/umthydromodeling/dawuaphydroengine',
    'download_url': 'https://bitbucket.org/umthydromodeling/dawuaphydroengine/get/a88ac8f68b01.zip',
    'include_package_data': True,
    'install_requires': [ # NOTE: Must be "tables" for PyPI
        'matplotlib', 'numpy', 'rasterio', 'rasterstats', 'fiona', 'shapely', 'tqdm', 'scipy', 'pandas', 'tables', 'fire'
    ],
    'extras_require': {
        'test': ['nose', 'mock']
    },
    'packages': [
        'daWUAP', 'daWUAP.assimilation', 'daWUAP.econengine', 'daWUAP.hydroengine', 'daWUAP.plotting', 'daWUAP.utils'
    ],
    'py_modules': [
        'hyena',
    ],
    'package_data': {'utils': ['*.txt']},
    'scripts': [
        'daWUAP/hyena.py',
        'bin/dataCollectionThredds.py',
        'bin/writeVectorModelParameters.py',
        'bin/writeRasterModelParameters.py'
    ],
    #'ext_modules': cythonize("hydroengine/hydroengine.py"),
    #'zip_safe': False
}

setup(**config)
