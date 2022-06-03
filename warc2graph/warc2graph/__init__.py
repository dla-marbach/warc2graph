# This file is part of warc2graph.
#
# warc2graph is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# warc2graph is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with warc2graph.  If not, see <https://www.gnu.org/licenses/>.

"""
warc2graph
==========

Warc2graph extracts a graph data structure from WARC files. The module was built to dig deeper into WARC files.
It extracts (almost) all internal and external references from a WARC file by analyzing the WARC header and the payload.


Functions
---------
create_graph(input_data, input_type="warc", methods="all", merge_results=True, blacklist=None, store_content=True, count_tags=False, collect_metadata=True, metadata=None, tagset="all", custom_tagset=None)
    Creates a networkx.DiGraph (directed graph network) representing archived or live websites.

extract_links(input_data, input_type="warc", methods="all", merge_results=True, blacklist=None, store_content=True, count_tags=False, collect_metadata=True, tagset="all", custom_tagset=None)
    Extracts all links from (archived) website.

links2graph(links, metadata=None, node_attributes=None)
    Creates a networkx DiGraph (directed graph network) from a list of links.
"""

import pkg_resources  # part of setuptools
__version__ = pkg_resources.require("warc2graph")[0].version


# make most important functions available in general scope
from warc2graph.warc2graph import create_graph
from warc2graph.linkextraction import extract_links
from warc2graph.graphs import links2graph
