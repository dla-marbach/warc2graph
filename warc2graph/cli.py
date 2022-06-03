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

from warc2graph import warc2graph

import networkx as nx
import matplotlib.pyplot as plt

import sys
import os
from argparse import ArgumentParser
import json


# ====================================================
desc = "Creates network graph representing archived or live websites."
parser = ArgumentParser(description=desc)
parser.add_argument("data_path", type=str, metavar="DATA-PATH",
                    help="path to a warc file or to a text file containing one url in each row")
parser.add_argument("data_type", type=str, choices=["w", "ll", "wl", "d"], default="w", metavar="DATA-TYPE", nargs="?",
                    help="type of input data, 'w' for warc file, 'd' for a url pointing to a warc file, 'wl', and 'll' \
                    for a text file containing one url to a live webpage in each row")
parser.add_argument("-o", "--output-path", type=str, metavar="OUTPUT-PATH",
                    help="directory where output will be stored",
                    default=".")
parser.add_argument("-k", "--blacklist", type=str,
                    help="path to a file containing one blacklisted domain in each row",
                    default=None)
parser.add_argument("-c", "--store-content", action="store_const", const=True, default=False,
                    help="include html content")
parser.add_argument("-m", "--collect_metadata", action="store_const", const=True, default=False,
                    help="extract meta data and extracted text from html")
parser.add_argument("-V", "--create-visualisation", action="store_const", const=True, default=False,
                    help="create and store a visualisation for the created network")
parser.add_argument("-v", "--verbose", action="store_const", const=True, default=False,
                    help="be verbose about what is going on")
parser.add_argument("--version", action="version", version="%(prog)s " + __import__("warc2graph").__version__)

args = parser.parse_args()


# ====================================================
def main():
    # validate and reformat arguments
    if args.data_type == "w":
        data_type = "warc"
    elif args.data_type == "d":
        data_type = "download"
    elif args.data_type == "wl":
        data_type = "warc_list"
    elif args.data_type == "ll":
        data_type = "live_list"

    is_warc = "warc.gz" in args.data_path[-len("warc.gz"):]
    if (data_type == "live" and is_warc) or ((data_type == "warc" or data_type == "download") and not is_warc):
        raise ValueError(
            f"data-type and data-path don't fit. '{args.data_path}' is {'not ' if data_type == 'warc' else ''}\
    a warc file.")

    if data_type in ["warc_list", "live_list"]:
        with open(args.data_path) as inf:
            input_data = inf.readlines()
        input_data = [dp.rstrip() for dp in input_data]
    else:
        input_data = args.data_path

    if args.blacklist is None:
        blacklist = None
    else:
        with open(args.blacklist) as blacklist_file:
            blacklist = [b.rstrip() for b in blacklist_file]

    # ====================================================
    # call principal function
    if not args.verbose:
        with open("/dev/null", "w") as out:
            stdout = sys.stdout
            sys.stdout = out
            try:
                model = warc2graph.create_graph(input_data=input_data, input_type=data_type, blacklist=blacklist,
                                                store_content=args.store_content,
                                                collect_metadata=args.collect_metadata)
            finally:
                sys.stdout = stdout
    else:
        model = warc2graph.create_graph(input_data=input_data, input_type=data_type, blacklist=blacklist,
                                        store_content=args.include_content, collect_metadata=args.collect_metadata)

    # write output to file
    if args.output_path != ".":
        directory = os.path.dirname(args.output_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    timestamp = model.graph["graph_metadata"]["timestamp"]
    gexf_path = os.path.join(args.output_path, f"{timestamp}_graph.gexf")
    meta_path = os.path.join(args.output_path, f"{timestamp}_metadata.json")
    visu_path = os.path.join(args.output_path, f"{timestamp}_visualisation.pdf")

    with open(gexf_path, "wb") as out_path:
        nx.readwrite.gexf.write_gexf(model, out_path)

    with open(meta_path, "w") as out_path:
        json.dump(dict(model.graph), out_path, indent=4)

    if args.create_visualisation:
        shallow_model = nx.DiGraph()
        shallow_model.add_edges_from(model.edges)
        fig, ax = plt.subplots(1, figsize=(8, 4))
        try:
            pos = nx.drawing.nx_agraph.graphviz_layout(shallow_model, prog="dot")
        except ImportError:
            errormsg = """You don't have graphviz installed or graphviz is not available in your path.
            Consider https://pygraphviz.github.io/documentation/stable/install.html for install instructions.
            For now, spring layout will be used.
            """
            print(errormsg, file=sys.stderr)
            pos = nx.drawing.layout.spring_layout(shallow_model)

        nx.draw_networkx(model, with_labels=False, pos=pos, ax=ax)
        fig.savefig(visu_path, dpi=300)


# ====================================================
if __name__ == "__main__":
    main()
