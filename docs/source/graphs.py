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
def create_network(*args, **kwargs) -> nx.DiGraph:
    print("'create_network' is deprecated. Please use 'link2graph' instead", file=sys.stderr)
    return links2graph(*args, **kwargs)

def get_random_ingredients(kind=None):
    """
    Return a list of random ingredients as strings.

    :param kind: Optional "kind" of ingredients.
    :type kind: list[str] or None
    :raise lumache.InvalidKindError: If the kind is invalid.
    :return: The ingredients list.
    :rtype: list[str]

    """

def links2graph(links, metadata=None, node_attributes=None) -> nx DiGraph:
    """
    Creates DiGraph f networkx (directed graph network) from list of links.
    
    :param list links: List of tuples, that contain two urls, the type of the link and possibly contents (depending on include_content).
    :param dict metadata: (optional) Metadata of the object. These will be implemented as attributes of the graph.
    :param dict node_attributes: (optional) Dict containing attributes, that shall be added to the nodes. Must be a in the shape of {node:{attribute_key: attribute_value}}.
	:return: A DiGraph from networkx modelling the input is returned.
	:rtype: int
	
	.. deprecated:: 'create_network' is deprecated. Please use 'link2graph' instead.
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
