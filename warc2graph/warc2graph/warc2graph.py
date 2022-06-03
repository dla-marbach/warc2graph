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
import os.path
import sys

from warc2graph import linkextraction
from warc2graph import graphs
from warc2graph import __version__

from datetime import datetime
import time

import networkx as nx


def create_model(*args, **kwargs):
    """
    .. deprecated:: 0.2

    The function 'create_model' has been replaced by 'create_graph'.
    """
    print(file=sys.stderr)
    return create_graph(*args, **kwargs)


def create_graph(input_data, input_type="warc", methods="all", merge_results=True, blacklist=None,
                 store_content=True, count_tags=False, collect_metadata=True, metadata=None, tagset="all",
                 custom_tagset=None) -> nx.DiGraph:
    """This is the main function of warc2graph.
    It creates a NetworkX DiGraph representing archived or live websites, modelling the input or a dict with methods as keys and corresponding generated models as NetworkX DiGraph as values.
    A NetworkX DiGraph is a directed graph, that is, a graph with directed edges. See NetworkX documentation for further information, >https://networkx.org/documentation/stable/reference/index.html<.
    
    Parameters
    ----------
    input_data : str or list
        The data that is to be modelled. Either:

        - a path to a local warc file,
        - a url to an online warc file,
        - a path to a list of multiple warc files, or
        - a path to a list of links to the live web

    input_type : {'warc', 'download', 'warc_list', 'live_list'}, default: 'warc'
        Declares the type of the input explicitly. Either:

        - 'warc' if input_data is a path to a local warc file
        - 'download' if input_data is an url to an online warc file
        - 'warc_list' if input_data is a path to a list of multiple warc files. If you want to create a model using a list of warc files all together archiving one big website, first create a list of all the warc files as txt-file. It should look as follows:
            * path/to/warc1.warc.gz
            * path/to/warc2.warc.gz
            * path/to/warc3.warc.gz
        - 'live_list' if input_data is a path to a list of links to the lives. You can also model a website that is not archived. Create a plain text file containing the urls to all the webpages you want to consider. This file should look as follows:
            * url/to/webpage1.html
            * url/to/webpage2.html
            * url/to/webpage3.html

    methods : {'all', 'wmd', 'bs4', 'rep'} or list, default: 'all'
        Which method or methods should be used for link extraction? Currently implemented:

        - 'wmd': This method reads out the metadata stored in the WARC file.
            If input_type is 'warc', also set parameter store_content 'False'.
            If input_type is 'live_list' this method is not available.
        - 'bs4': This method analysez the HTML data using the python library BeautifulSoup.
            If input_type is 'warc', also set parameter collect_metadata 'False'.
        - 'rep': In order to also evaluate JavaScript the HTML data is processed with the remote controlled headless browser Selenium.
            If input_type is 'warc', Geckodriver will be installed if necessary. If an error message appears that Geckodriver cannot be installed, try installing the correct version of Geckodriver manually. To do this, you should download the current version of Geckodriver and move it to the appropriate file folder. You will have to repeat this procedure every time a new version of Geckodriver is available.
        - 'all': Uses all methods 'wmd', 'bs4', and 'rep'.
        - subset: If a list containing a subset of these methods is set, also set parameter merge_results 'True'.

    merge_results : bool, default: True
        Whether the results of methods should be merged to one result.

        - If 'True', the results of methods will be merged to one result.
        - If 'False', the output will be a dict containing results for different methods.
    
    blacklist : list, default: None
        List of domains that will be ignored.

    store_content : bool, default: True
        Whether the html-text should be stored in the model.

        - If 'True', a dict containing this info will be added to the output, so the output will be a tuple.

    count_tags : bool, default: False
        Whether counts of all tags should be stored in the model.

        - If 'True', all tags on every page will be counted and a dict containing this info will be added to the output, so the output will be a tuple.

    collect_metadata : bool, default: True
        Whether plaintext (with removed boilerplates), title, date and author should be extracted from each html. See `Trafilatura <https://trafilatura.readthedocs.io/en/latest/#further-documentation>`_ for further information.

    metadata : dict, default: None
        Metadata describing the whole website can be added to the model, no specific keys are determined.
        If nothing is given, the name of the (first) warc file or the first url will be stored as filename.

    tagset : {'all', 'a_only', 'html_only', 'no_scripts', 'custom'}, default: 'all'
        Choose the set of tags you want to use:

        - 'a_only': Extracts hyperlinks only from the <a> tag. That is [("a", "href")].
        - 'html_only': Extracts hyperlinks that refer only to html-files. That is [("a", "href"), ("frame", "src"), ("iframe", "src"), ("link", "href"), ("base", "href"), ("meta", "url"), ("area", "href"), ("form", "action"), ("button", "formation"), ("q", "cite"), ("blockquote", "cite")].
        - 'no_scripts': Extracts all hyperlinks except the <script> tag. That is [("a", "href"), ("frame", "src"), ("iframe", "src"), ("link", "href"), ("base", "href"), ("object", "data"), ("img", "src"), ("applet", "object"), ("embed", "src"), ("meta", "url"), ("meta", "content"), ("audio", "src"), ("video", "src"), ("area", "href"), ("form", "action"), ("button", "formation"), ("q", "cite"), ("blockquote", "cite")].
        - 'all': Extracts all hyperlinks. That is [("a", "href"), ("frame", "src"), ("iframe", "src"), ("link", "href"), ("base", "href"), ("object", "data"), ("img", "src"), ("applet", "object"), ("embed", "src"), ("meta", "url"), ("meta", "content"), ("audio", "src"), ("video", "src"), ("script", "src"), ("area", "href"), ("form", "action"), ("button", "formation"), ("q", "cite"), ("blockquote", "cite")].
        - 'custom': Give any HTML tag you want to extract the links from. If this is chosen, also set parameter 'custom_tagset'.

    custom_tagset : list, default: None
        If tagset is set to 'custom', give a list of tuples containing the tag and the attribute you want to extract the links from.


    Returns
    -------
    networkx.DiGraph or dict
        If merge_results is 'True' or results are only generated using one method, a NetworkX DiGraph modelling the input is returned.
        If merge_results is 'False' it returns a dict with methods as keys and corresponding generated models as NetworkX DiGraph as values.
    """
    parameters = locals()  # store for metadata

    # measure runtime
    start = time.time()

    # get links
    links, node_attributes = linkextraction.extract_links(input_data, input_type, methods, merge_results, blacklist,
                                                          store_content, count_tags, collect_metadata, tagset,
                                                          custom_tagset)

    # prepare metadata
    if metadata is None:
        if type(input_data) is not list:
            name = input_data
        else:
            name = input_data[0]

        work_md = {"file_name": os.path.basename(name)}

    else:
        work_md = metadata
        if "file_name" not in work_md:
            if type(input_data) is not list:
                name = input_data
            else:
                name = input_data[0]
            work_md["file_name"] = os.path.basename(name)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    graph_md = {"timestamp": timestamp, "version": __version__, "parameters": parameters}

    # create graph(s)
    if not merge_results:
        output = {}
        for method, met_links in links.items():
            print(method)
            metadata = {"work_metadata": dict(work_md), "graph_metadata": dict(graph_md)}
            output[method] = graphs.links2graph(met_links, metadata, node_attributes)

            # create more metadata
            output[method].graph["graph_metadata"]["method"] = method
            print(len(output[method].nodes))
            output[method].graph["graph_metadata"]["n_nodes"] = len(output[method].nodes)
            output[method].graph["graph_metadata"]["n_edges"] = len(output[method].edges)
            runtime = time.time() - start
            output[method].graph["graph_metadata"]["runtime"] = round(runtime, 3)

    else:
        metadata = {"work_metadata": dict(work_md), "graph_metadata": dict(graph_md)}
        output = graphs.links2graph(links, metadata, node_attributes)

        # create more metadata
        output.graph["graph_metadata"]["method"] = output.graph["graph_metadata"]["parameters"]["methods"]
        output.graph["graph_metadata"]["n_nodes"] = len(output.nodes)
        output.graph["graph_metadata"]["n_edges"] = len(output.edges)
        runtime = time.time() - start
        output.graph["graph_metadata"]["runtime"] = round(runtime, 3)

    return output
