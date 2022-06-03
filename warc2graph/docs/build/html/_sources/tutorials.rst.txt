.. _tutorials:

========
Tutorial
========

This tutorial will help you to create and plot a basic graph from a warc file.

Preparation
-----------

Import warc2graph and other modules.

.. code-block:: python

	import warc2graph as w2g # our package
	import matplotlib.pyplot as plt # plot graphs
	import networkx as nx # handle graphs
	from pprint import PrettyPrinter  # print dicts nicely
	pp = PrettyPrinter()

Set path
--------

Assign a variable to the path of a warc file.

.. code-block:: python

	warc_path = "tests/WEB-20210202165627638-00000-24143~clarin02~8443.warc.gz"

Create graph
------------

Create a basic graph with all resources as nodes and all links and embeddings as edges.

.. code-block:: python

	basic_model = w2g.create_graph(warc_path)

Visualise graph
---------------

Visualise the graph using the graphviz *dot* algorithm.

.. code-block:: python

	fig, ax = plt.subplots(1, figsize=(8, 4))
	pos = nx.drawing.nx_agraph.graphviz_layout(basic_model, prog="dot")
	nx.draw_networkx(basic_model, with_labels=False, pos=pos, ax=ax)
	plt.draw()
	
Calculate centrality metrics
----------------------------

Calculate the degree centrality for all nodes.

.. code-block:: python

	pp.pprint(nx.algorithms.centrality.degree_centrality(basic_model))

You can also calculate any other centrality metric or any other graph related metric implemented in networx with ease.


Enriched models
---------------

Create an enriched model, structured like the basic model but containing the html content and counts of all tags.

.. code-block:: python

	enriched_model = warc2graph.create_graph(warc_path, include_content=True, count_tags=True)

Checking the data in the enriched model
---------------------------------------

If you included the content or meta data in the graph, you can retrieve this data as follows:

.. code-block:: python

	index_node = "https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html"
	print(f"counted tags from '{index_node}:\n'")
	print(enriched_model.nodes[index_node]["counted_tags"])


.. code-block:: python

	index_node = "https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html"
	print(f"content of '{index_node}':\n")
	print(enriched_model.nodes[index_node]["content"])


Visualizing the graph you can see, that it is structurally the same. Sadly graphviz hiccups with html in an attribute, so we have to remove the content before calculating positions.

.. code-block:: python

	fig, ax = plt.subplots(1, figsize=(8, 4))
	enriched_model_wo_content = nx.DiGraph(enriched_model)
	for node in enriched_model_wo_content.nodes:
		enriched_model_wo_content.nodes[node].pop("content", None)
		pos = nx.drawing.nx_agraph.graphviz_layout(enriched_model_wo_content, prog="dot")
		nx.draw_networkx(enriched_model, with_labels=False, pos=pos, ax=ax)
	plt.draw()


Compare different methods
-------------------------

Graphs for different methods can be compared.

.. code-block:: python

	methods = ["bs4", "wmd", "rep"]
	fig, axes = plt.subplots(3, figsize=(8, 14))
	for method, ax in zip(methods, axes):
		model = warc2graph.create_graph(warc_path, methods=method)
		pos = nx.drawing.nx_agraph.graphviz_layout(model, prog="dot")
		nx.draw_networkx(model, with_labels=False, pos=pos, ax=ax)
		ax.set_title(method)
	plt.draw()

Downloads
=========

* `Download this page as a Jupyter notebook <https://clarin06.ims.uni-stuttgart.de/sdc4lit/warc2graph/-/blob/master/examples.ipynb>`_
