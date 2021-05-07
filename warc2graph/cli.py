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
from itertools import permutations
import matplotlib.pyplot as plt

import sys
import os
from argparse import ArgumentParser
import json


# ====================================================
desc = "Creates graph network based models of websites. It was built to analyze the narrative structure of\
net-literature from the 90s and 00s."
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
parser.add_argument("-c", "--include-content", action="store_const", const=True, default=False,
                    help="include text and other media to model")
method_choices = ["".join(p) for r in range(1, 4) for p in permutations(["w", "b", "r"], r)] + ["a"]
parser.add_argument("-m", "--methods", type=str, choices=method_choices,
                    metavar="METHOD",
                    help="methods to be used to extract links, 'w' for metadata from warc file, 'b' for parsed html, \
                    'r' for replay using selenium browser; if two methods are wanted give both letters, \
                    for all methods 'a', if 'r' is selected, Geckodriver will be installed if necessary",
                    default="a")
parser.add_argument("-V", "--create-visualisation", action="store_const", const=True, default=False,
                    help="create and store a visualisation for the created network")
parser.add_argument("-d", "--dont-merge-results", action="store_const", const=True, default=False,
                    help="if passed, an output file for each method will be created instead of the results being\
                     merged")
parser.add_argument("-b", "--base-object", type=str, choices=["r", "p", "m"],
                    help="object to be taken as base for model – What should be represented by a node? \
                     'r' for resource, 'p' for webpage and 'm' for moment during inspection", default="r")
parser.add_argument("-v", "--verbose", action="store_const", const=True, default=False,
                    help="be verbose about what is going on")
parser.add_argument("--version", action="version", version="%(prog)s "+ __import__("warc2graph").__version__)

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

    methods = []
    for m in args.methods:
        if m == "a":
            methods = "all"
        elif m == "w":
            methods.append("wmd")
        elif m == "b":
            methods.append("bs4")
        elif m == "r":
            methods.append("rep")

    if args.blacklist is None:
        blacklist = None
    else:
        with open(args.blacklist) as blacklist_file:
            blacklist = [b.rstrip() for b in blacklist_file]

    if args.base_object == "r":
        base_object = "resource"
    elif args.base_object == "p":
        base_object = "page"
    else:
        base_object = "moment"

    # ====================================================
    # call principal function
    if not args.verbose:
        with open("/dev/null", "w") as out:
            stdout = sys.stdout
            sys.stdout = out
            try:
                model = warc2graph.create_model(input_data=input_data, input_type=data_type,
                                                methods=methods, merge_results=not args.dont_merge_results,
                                                blacklist=blacklist, base_object=base_object,
                                                include_content=args.include_content)
            finally:
                sys.stdout = stdout
    else:
        model = warc2graph.create_model(input_data=input_data, input_type=data_type,
                                        methods=methods, merge_results=not args.dont_merge_results,
                                        blacklist=blacklist, base_object=base_object,
                                        include_content=args.include_content)

    # write output to file
    if args.output_path != ".":
        directory = os.path.dirname(args.output_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    if not args.dont_merge_results:
        model = {"all": model}

    for method, method_model in model.items():
        timestamp = method_model.graph["graph_metadata"]["timestamp"]
        methodstamp = "_" + method if method != "all" else ""
        gexf_path = os.path.join(args.output_path, f"{timestamp}_graph{methodstamp}.gexf")
        meta_path = os.path.join(args.output_path, f"{timestamp}_metadata{methodstamp}.json")
        visu_path = os.path.join(args.output_path, f"{timestamp}_visualisation{methodstamp}.pdf")

        with open(gexf_path, "wb") as out_path:
            nx.readwrite.gexf.write_gexf(method_model, out_path)

        with open(meta_path, "w") as out_path:
            json.dump(dict(method_model.graph), out_path, indent=4)

        if args.create_visualisation:
            fig, ax = plt.subplots(1, figsize=(8, 4))
            try:
                pos = nx.drawing.nx_agraph.graphviz_layout(method_model, prog="dot")
            except ImportError:
                errormsg = """You don't have graphviz installed or graphviz is not available in your path.
                Consider https://pygraphviz.github.io/documentation/stable/install.html for install instructions.
                For now, circular layout will be used.
                """
                print(errormsg, file=sys.stderr)
                pos = nx.drawing.layout.spring_layout(method_model)

            nx.draw_networkx(method_model, with_labels=False, pos=pos, ax=ax)
            fig.savefig(visu_path, dpi=300)


# ====================================================
if __name__ == "__main__":
    main()
