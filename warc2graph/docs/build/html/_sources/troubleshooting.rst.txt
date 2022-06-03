.. _troubleshooting:

================
Troubleshooting
================

PygraphViz
==========

If you have difficulty :ref:`installing PygraphViz <install_extra_packages>`, try to install `GraphViz <https://graphviz.org/download/>`_ first. For Mac this would be:

.. code-block:: console

	brew install graphviz
	python -m pip install pygraphviz

If that doesn't work, try also:

.. code-block:: console
	
	brew doctor
	brew install graphviz
	python -m pip install pygraphviz
