.. _installation:

============
Installation
============

The output when using the CLI consists of graph data in a standard graph XML format GEXF and several visualizations of that data using different visualization algorithms. We acknowledge that visualizations carry an epistemic value and thus need to be designed according to the analyzed objects and research questions.

Warc2graph requires Python 3.6+ and is available from:

* `GitHub <https://github.com/dla-marbach/warc2graph.git>`_

Install warc2graph with pip
===========================

Use the Python package manager `pip <https://pip.pypa.io/en/stable/>`_ to install the current release of warc2graph.
If you do not have the latest version of pip, upgrade pip first.

.. code-block:: console

	python -m pip install warc2graph
	
To upgrade warc2graph to a newer release use:

.. code-block:: console

	python -m pip install --upgrade warc2graph

Install warc2graph with setuptools
==================================

Alternatively you can install manually using the python package `setuptools <https://pypi.org/project/setuptools/>`_.

.. code-block:: console

	git clone https://github.com/dla-marbach/warc2graph.git
	cd warc2graph
	python setup.py build
	python setup.py install --user

.. _install_extra_packages:

Install extra packages
======================

To be able to use the dot algorithm to visualize the graph, make sure, to have `PyGraphviz <https://pygraphviz.github.io/documentation/stable/install.html>`_ (via `GraphViz <https://graphviz.org/download/>`_) installed.
We recommend to create a `Python virtual environment <https://docs.python.org/3/library/venv.html>`_ to install the required packages.
If you have trouble with the installation, check out the :doc:`troubleshooting` section.

.. code-block:: console

	python -m pip install pygraphviz

Requirements
============

warc2graph requires these programms:

* `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_ >= 4.9.3
* `lxml <https://lxml.de>`_ >= 4.6.0
* `matplotlib <https://matplotlib.org>`_ >= 3.3.3
* `NetworkX <https://networkx.org>`_ >= 2.5
* `NumPy <https://numpy.org>`_ == 1.19.5
* `Selenium <https://www.selenium.dev>`_ >= 3.141.0
* `Setuptools <https://setuptools.pypa.io/en/latest/>`_ >= 51.0.0
* `Warcio <https://github.com/webrecorder/warcio>`_ >= 1.7.4
* `webdriver-manager <https://github.com/SergeyPirogov/webdriver_manager>`_ >= 3.3.0
* `trafilatura <https://trafilatura.readthedocs.io/en/latest/>`_ >= 0.9.0
