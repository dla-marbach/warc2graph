======================================
Welcome to warc2graph's documentation!
======================================

warc2graph
==========

Warc2graph extracts a graph data structure from WARC (Web ARChive) files.
The module was built to dig deeper into WARC files. It extracts (almost) all internal and external references from a WARC file by analyzing the WARC header and the payload. Multiple methods can be used for extraction, single or combined.

The initial purpose of warc2graph was to analyze and visualize the textual structure of net literature works in the `DLA corpus of net literature works and blogs <http://literatur-im-netz.dla-marbach.de>`_ dating from the early time of the web in the 1990s up to the 2000s.
Development is part of the `Science Data Center for Literature <https://www.sdc4lit.de>`_ research project. We now consider warc2graph as a tool for detailed WARC analytics regarding the referential structure of the archived sites and hope that it will be useful for the web archiving and web research community.
	
Warc2graph has a CLI interface and can be used as a python module.
Check out the :doc:`usage` section for further information.

Warc2graph is under active development.

If you consider using warc2graph for a research project or in an archival context, please :doc:`get_in_touch`! We'd love to hear about your work.

Warc2graph has been presented at the Electronic Literature Organization Conference 2020: `Overview and Video <https://elmcip.net/critical-writing/networks-net-literature-modelling-extracting-and-visualizing-link-based-networks>`_ | `Conference Paper (PDF) <https://elmcip.net/sites/default/files/media/critical_writing/attachments/claus-michael_schlesinger_mona_ulrich_pascal_hein_and_andre_blessing_networks_of_net_literature_-_modelling_extracting_and_visualizing_192.pdf>`_

Contributing
============

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

All contributed Code will be licensed under the GNU Lesser General Public License.

By contributing you accept the following terms and conditions:

* You grant the rights for your contribution to be used, distributed and modified together with warc2graph and under the same license.
* Your contribution consists of your work, no third party holds rights over it.
* You grant us the right to redistribute the software including your contribution under a different (permissive or non-permissive) open source license.

Citing
======

Warc2graph has been presented at the Electronic Literature Organization Conference 2020: `Overview and Video <https://elmcip.net/critical-writing/networks-net-literature-modelling-extracting-and-visualizing-link-based-networks>`_ | `Conference Paper (PDF) <https://elmcip.net/sites/default/files/media/critical_writing/attachments/claus-michael_schlesinger_mona_ulrich_pascal_hein_and_andre_blessing_networks_of_net_literature_-_modelling_extracting_and_visualizing_192.pdf>`_

License
=======

Warc2graph is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Warc2graph is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the `GNU Lesser General Public License <https://www.gnu.org/licenses/lgpl-3.0.html>`_ for more details. You should have received a copy of it along with warc2graph. If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

Consider `COPYING <https://clarin06.ims.uni-stuttgart.de/sdc4lit/warc2graph/-/blob/master/COPYING>`_ and `COPYING.LGPL <https://clarin06.ims.uni-stuttgart.de/sdc4lit/warc2graph/-/blob/master/COPYING.LGPL>`_.

Acknowledgement
===============

Warc2graph makes heavy and critical use of following open source libraries:

* `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_
* `matplotlib <https://matplotlib.org>`_
* `lxml <https://lxml.de>`_
* `NetworkX <https://networkx.org>`_
* `NumPy <https://numpy.org>`_
* `Selenium <https://www.selenium.dev>`_
* `setuptools <https://pypi.org/project/setuptools/>`_
* `Warcio <https://github.com/webrecorder/warcio>`_
* `webdriver-manager <https://github.com/SergeyPirogov/webdriver_manager>`_
* `trafilatura <https://trafilatura.readthedocs.io/en/latest/>`_


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. toctree::
    :maxdepth: 2
    :hidden:
	
    installation
    usage
    basic_functions
    tutorials
    troubleshooting
    get_in_touch
