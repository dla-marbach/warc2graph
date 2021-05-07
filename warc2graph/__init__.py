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
create_model(input_data, input_type="warc", methods="all", merge_results=True, blacklist=None,
             base_object="resource", include_content=False, count_tags=False, metadata=None)
    Creates a graph network based model of a website.

extract_links(input_data, input_type="warc", methods="all", merge_results=True, blacklist=None,
              include_content=False, count_tags=False)
    Extract all the connections between resources in a warc file.

create_network(links, metadata=None, base_object="resource", node_attributes=None)
    Create a networkx DiGraph from a list of links.

"""

import pkg_resources  # part of setuptools
__version__ = pkg_resources.require("warc2graph")[0].version


# make most important functions available in general scope
from warc2graph.warc2graph import create_model
from warc2graph.linkextraction import extract_links
from warc2graph.networks import create_network
