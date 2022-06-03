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

from warc2graph import graphs
import unittest
import networkx as nx


class TestNetworksMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.g = nx.DiGraph()
        cls.edges = [("1", "2", {"type": "frame"}), ("2", "3", {"type": "frame"}), ("3", "4", {"type": "a"}),
                 ("2", "5", {"type": "a"})]
        cls.g.add_edges_from(cls.edges)
        super().setUpClass()

    def test_create_network(self):
        silver = graphs.links2graph(self.edges)
        self.assertTrue(nx.is_isomorphic(silver, self.g))


if __name__ == "__main__":
    unittest.main()
