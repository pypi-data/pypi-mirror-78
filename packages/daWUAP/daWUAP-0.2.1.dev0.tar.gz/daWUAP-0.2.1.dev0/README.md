daWUAP - data assimilation Water Use and Agricultural Productivity Model
========================================================================

The data assimilation Water Use and Agricultural Productivity model (daWUAP) is a hydro-economic model that couples an economic model of agricultural production calibrated using positive mathematical programming (PMP) and a semidistributed rainfall-runoff-routing model that simulates water available to producers.

Features:

* Calibration of economic component can use standard the mathematical programming method or a new recursive stochastic filter.
* Stochastic calibration permits to obtain simulation results of agricultural outputs (land and water allocation, etc) as probability distributions that reflect the quality of the calibration.
* Recursive stochastic filter permits calibration of economic model with noisy but frequent remote sensing observations of agricultural activity.
* Model permits to trace the effect of producer choices on the hydrologic system and on other users.

Contributions and comments are welcome [on our Bitbucket repository](https://bitbucket.org/umthydromodeling/dawuap.git).


Dependencies
============

Please note that daWUAP requires:

* Python >= 3.7
* `GDAL support <https://gdal.org/>` (version 1.13 or higher)
* `HDF5 support <https://www.hdfgroup.org/solutions/hdf5/>`


Installation
============

There are multiple ways to install the `dawuap` Python package.


Installation from Source
------------------------

It is recommended that you install the package in a virtual environment, either with `virtualenv` or `conda`. In general:

1. Download or clone repository;
2. Change your working directory (`cd`) to the repository directory;
3. `python setup.py install`

**Or, with `pip`:**

1. Download or clone repository;
2. Change your working directory (`cd`) to the repository directory;
3. `pip install .`

**Or, for installation using `conda`:**

1. Download or clone repository;
2. Change your working directory (`cd`) to the repository directory;
3. Create a new environment: `conda create --name dawuap python=3`
4. Activate the environment: `source activate dawuap`
5. `conda install .`


Installation from Source (for Developers)
-----------------------------------------

If you plan to make changes to the source code, it's most convenient to install daWUAP in "editable" mode.

Using `pip` (preferably in a virtual environment), from the top-level directory of the repository:

``
pip install -e .
``

If you use `conda` to create and manage your virtual environments, be sure to `conda install pip` before running the above.


Testing
-------

```
python daWUAP/tests/tests.py
```


Documentation
=============

The documentation available as of the date of this release is included in HTML format in the Documentation directory of the repository. `The most up-to-date documentation can be found here. <https://dawuap.readthedocs.io/en/latest/>`


Input Vector File Schema
------------------------

All input vector datasets need to have a standard schema. For the basins attributes (or "properties"):

``
'FROM_NODE', 'TO_NODE', 'SUBBASIN', 'SUBBASINR', 'AREAC', 'hbv_ck0', 'hbv_ck1', 'hbv_ck2', 'hbv_hl1', 'hbv_perc', 'hbv_pbase'
``

For the river or network attributes:

``
'ARCID', 'FROM_NODE', 'TO_NODE', 'SUBBASIN', 'SUBBASINR', 'AREAC', 'k', 'es'
``

In particular, "SHAPE_AREA" (if present), "ARCID", "SUBBASIN" must be in all upper-case. Currently, "ARCID" and "SUBBASIN" are the unique identifiers for stream/ network segments and subsheds, respectively.


Licensing
=========

  Please see the file called LICENSE.txt.


Bugs & Contribution
===================

[Please use Bitbucket](https://bitbucket.org/umthydromodeling/dawuap/issues) to report any bugs, to ask questions, or to submit pull requests.
