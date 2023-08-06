|PyPI package| |Documentation| |Test results| |Test coverage| |Code
analysis| |License| |Analytics|

Whole-cell modeling utilities
=============================

This package contains utilities that are useful to multiple whole-cell
(WC) software components.

Installation
------------

1. Install the third-party dependencies listed below. Detailed
   installation instructions are available in `An Introduction to
   Whole-Cell
   Modeling <http://docs.karrlab.org/intro_to_wc_modeling/master/0.0.1/installation.html>`__.

   -  `ChemAxon Marvin <https://chemaxon.com/products/marvin>`__:
      optional to calculate major protonation states
   -  `Java <https://www.java.com>`__ >= 1.8
   -  `Git <https://git-scm.com/>`__
   -  `OpenBabel <http://openbabel.org>`__: optional to calculate
      chemical formulae
   -  `Pip <https://pip.pypa.io>`__ >= 18.0
   -  `Python <https://www.python.org>`__ >= 3.6

2. To use Marvin to calculate major protonation states, set
   ``JAVA_HOME`` to the path to your Java virtual machine (JVM)
   ``export JAVA_HOME=/usr/lib/jvm/default-java``

3. To use Marvin to calculate major protonation states, add Marvin to
   the Java class path
   ``export CLASSPATH=$CLASSPATH:/opt/chemaxon/marvinsuite/lib/MarvinBeans.jar``

4. Install this package

   -  Install the latest release from PyPI ``pip install wc_utils[all]``

   -  Install the latest revision from GitHub
      ``pip install git+https://github.com/KarrLab/pkg_utils.git#egg=pkg_utils[all]   pip install git+https://github.com/KarrLab/wc_utils.git#egg=wc_utils[all]``

Example usage
-------------

Documentation
-------------

Please see the `API documentation <http://docs.karrlab.org/wc_utils>`__.

License
-------

The build utilities are released under the `MIT license <LICENSE>`__.

Development team
----------------

This package was developed by the `Karr Lab <http://www.karrlab.org>`__
at the Icahn School of Medicine at Mount Sinai in New York, USA.

-  Arthur Goldberg
-  Jonathan Karr

Questions and comments
----------------------

Please contact the `Karr Lab <http://www.karrlab.org>`__ with any
questions or comments.

.. |PyPI package| image:: https://img.shields.io/pypi/v/wc_utils.svg
   :target: https://pypi.python.org/pypi/wc_utils
.. |Documentation| image:: https://readthedocs.org/projects/wc-utils/badge/?version=latest
   :target: http://docs.karrlab.org/wc_utils
.. |Test results| image:: https://circleci.com/gh/KarrLab/wc_utils.svg?style=shield
   :target: https://circleci.com/gh/KarrLab/wc_utils
.. |Test coverage| image:: https://coveralls.io/repos/github/KarrLab/wc_utils/badge.svg
   :target: https://coveralls.io/github/KarrLab/wc_utils
.. |Code analysis| image:: https://api.codeclimate.com/v1/badges/8139298cdbc1e32dcde4/maintainability
   :target: https://codeclimate.com/github/KarrLab/wc_utils
.. |License| image:: https://img.shields.io/github/license/KarrLab/wc_utils.svg
   :target: LICENSE
.. |Analytics| image:: https://ga-beacon.appspot.com/UA-86759801-1/wc_utils/README.md?pixel

