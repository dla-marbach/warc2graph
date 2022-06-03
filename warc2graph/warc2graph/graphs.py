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
import sys

import networkx as nx


# ====================================================
def create_network(*args, **kwargs):
    """
    .. deprecated:: 0.2

    The function 'create_network' has been replaced by 'links2graph'.
    """
    print(file=sys.stderr)
    return links2graph(*args, **kwargs)


def links2graph(links, metadata=None, node_attributes=None) -> nx.DiGraph:
    """Creates NetworkX DiGraph (directed graph network) from list of links.
    
    Parameters
    ----------
    links : list
        List of tuples, that contain two urls, the type of the link and possibly contents (depending on include_content).
    
    metadata : dict, default: None
        Metadata of the object. These will be implemented as attributes of the graph.

    node_attributes : dict, default: None
        Dict containing attributes, that shall be added to the nodes. Must be a in the shape of {node:{attribute_key: attribute_value}}.

    Returns
    -------
    NetworkX DiGraph
        A NetworkX DiGraph (directed graph network) modelling the input is returned.
    """

    for link in links:
        if len(link) != 3 or type(link[2]) != dict:
            raise TypeError("links must be a list of tuples containing two strings (url-from and url-to) and one dict.")

    # print("Creating graph...")
    if metadata is not None:
        g = nx.DiGraph(**metadata)
    else:
        g = nx.DiGraph()

    for link in links:
        g.add_edge(link[0], link[1], **link[2])

    if node_attributes is not None and node_attributes != {}:
        nx.set_node_attributes(g, node_attributes)

    # print("Done.")
    return g
