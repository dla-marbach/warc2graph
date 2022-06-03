# warc2graph

Warc2graph extracts a graph data structure from WARC files. The module was built to dig deeper into WARC files. It extracts (almost) all internal and external references from a WARC file by analyzing the WARC header and the payload. Multiple methods can be used for extraction, single or combined. Warc2graph has a CLI interface and can be used as a python module. The output when using the CLI interface consists of graph data in a standard graph XML format GEXF and several visualizations of that data using different visualization algorithms. We acknowledge that visualizations carry an epistemic value and thus need to be designed according to the analyzed objects and research questions. Warc2graph uses [NetworkX](https://networkx.org/) as its graph data and analytics backend, so more involved graph data analytics can be realized when using warc2graph as a python module. 

The initial purpose of warc2graph was to analyze and visualize the textual structure of net literature works in the [DLA corpus of net literature works and blogs](http://literatur-im-netz.dla-marbach.de/) dating from the early time of the web in the 1990s up to the 2000s. Development is part of the [Science Data Center for Literature](https://sdc4lit.de) research project. We now consider warc2graph as a tool for detailed WARC analytics regarding the referential structure of the archived sites and hope that it will be useful for the web archiving and web research community. 

Warc2graph is under active development.

If you consider using warc2graph for a research project or in an archival context, please get in touch! We'd love to hear about your work. 

Warc2graph has been presented at the Electronic Literature Organization Conference 2020: \
| Overview and Video: <https://elmcip.net/critical-writing/networks-net-literature-modelling-extracting-and-visualizing-link-based-networks>
| Conference Paper (PDF): <https://elmcip.net/sites/default/files/media/critical_writing/attachments/claus-michael_schlesinger_mona_ulrich_pascal_hein_and_andre_blessing_networks_of_net_literature_-_modelling_extracting_and_visualizing_192.pdf>

## Installation

warc2graph requires Python >= 3.6.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install warc2graph.

```shell
pip install warc2graph
```

Alternatively you can install manually using the python package [setuptools](https://pypi.org/project/setuptools/).

```shell
git clone https://github.com/dla-marbach/warc2graph.git
cd warc2graph
python3 setup.py build
python3 setup.py install --user
```

To be able to use the dot algorithm to visualize the graph, make sure, to have [GraphViz](https://graphviz.org/) installed.

## Usage

You can use the package in your python projects, or you can use the provided command line interface. While the former
offers more possibilities, the latter might be more intuitive. 

### CLI

The installation of the package provides the `warc2graph` command for your terminal. Call `warc2graph --help` to get an
overview over the available options.

#### One warc file
If you want to create a model for only one warc file simply call
```shell
warc2graph path/to/warc.warc.gz
```

If the warc file is not on you file system, and you want it to be downloaded from the internet, you can pass an url. You 
have to pass the parameter `d`.

```shell
warc2graph url/to/warc.warc.gz d
```

#### List of warc files
If you want to create a model using a list of warc files all together archiving one big website, first create a list of
all the warc files.

```shell
ls path/to/warcs/*.warc.gz >> list_of_warcs.txt
```

You can also create the file manually, it should look as follows.
```
path/to/warc1.warc.gz
path/to/warc2.warc.gz
path/to/warc3.warc.gz
path/to/warc4.warc.gz
```

Then call warc2graph with the parameter `wl`, and the list as an input file.
```shell
warc2graph list_of_warcs.txt wl
```

#### List of live webpages
You can also model a website that is not archived. Create a plain text file containing the urls to all the webpages you
want to consider. This file should look as follows.

```
url/to/webpage1.html
url/to/webpage2.htm
```

Then call warc2graph with the parameter `ll`, and the list as an input file.

```shell
warc2graph list_of_webpages.txt ll
```

#### Further options
- methods to use
- create visualisation
- blacklist


### Python package
You can inspect the `examples.ipynb` using [jupyter notebook](https://jupyter.org/) for some interactive examples.

Our package relies heavily on the [networkx](https://networkx.org/) package. Read its documentation for further
information about the possibilities and interfaces for the analysis of networkx graphs. 

#### Creating and plotting a model

```python
import warc2graph  # our package
import matplotlib.pyplot as plt  # plot graphs
import networkx as nx  # handle graphs

# assign the path to a warc file to a variable
warc_path = "tests/WEB-20210202165627638-00000-24143~clarin02~8443.warc.gz"

# create a basic model with all resources as nodes and all links and embeddings as edges
basic_model = warc2graph.create_graph(warc_path)

# visualizing the graph using the graphviz "dot" algorithm
fig, ax = plt.subplots(1, figsize=(8, 4))
pos = nx.drawing.nx_agraph.graphviz_layout(basic_model, prog="dot")
nx.draw_networkx(basic_model, with_labels=False, pos=pos, ax=ax)
plt.draw()
```

![Visualized Graph](example.png "Visualized Graph")

#### Calculating different graph metrics

```python
import warc2graph  # our package
import networkx as nx  # handle graphs
from pprint import PrettyPrinter  # print dicts nicely

pp = PrettyPrinter()

warc_path = "tests/WEB-20210202165627638-00000-24143~clarin02~8443.warc.gz"
basic_model = warc2graph.create_graph(warc_path)
degree_centralities = nx.algorithms.centrality.degree_centrality(basic_model)

pp.pprint(degree_centralities)
```
Outputs:
```python
{'http://httpd.apache.org/': 0.07692307692307693,
 'http://www.scientificlinux.org/': 0.07692307692307693,
 'https://clarin09.ims.uni-stuttgart.de/': 0.23076923076923078,
 'https://clarin09.ims.uni-stuttgart.de/icons/apache_pb2.gif': 0.07692307692307693,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html': 0.23076923076923078,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html': 0.8461538461538463,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html': 0.23076923076923078,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/js/angular.min.js': 0.07692307692307693,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/js/jquery-1.11.3.min.js': 0.07692307692307693,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html': 0.15384615384615385,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html': 0.15384615384615385,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_ang1.html': 0.07692307692307693,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery1.html': 0.07692307692307693,
 'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery2.html': 0.07692307692307693}
```

#### Enriched models
You can also enrich the models using the original data.

```python
import warc2graph  # our package

# assign the path to a warc file to a variable
warc_path = "tests/WEB-20210202165627638-00000-24143~clarin02~8443.warc.gz"

# create an enriched model, structured like the basic model but containing the html content and counts of all tags
enriched_model = warc2graph.create_graph(warc_path, include_content=True, count_tags=True)

index_node = "https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html"
print(enriched_model.nodes[index_node]["counted_tags"])
# prints:
# {'html': 1, 'head': 1, 'meta': 1, 'title': 1, 'body': 1, 'a': 4, 'br': 6}

print(enriched_model.nodes[index_node]["content"])
```
Prints:
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>

<a href="page1.html">page1</a>

<br>
<br>
<a href="page2.html">page2</a>

<br>
<br>
<a href="angular1.html">angular1</a>


<br>
<br>
<a href="jquery.html">jquery</a>

</body>
</html>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

All contributed Code will be licensed under the GNU Lesser General Public License.

By contributing you accept the following terms and conditions:
* You grant the rights for your contribution to be used, distributed and modified together with warc2graph and under
  the same license.
* Your contribution consists of your work, no third party holds rights over it.
* You grant us the right to redistribute the software including your contribution under a different (permissive or
  non-permissive) open source license.

## License
warc2graph is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

warc2graph is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with warc2graph.  If not, see https://www.gnu.org/licenses/lgpl-3.0.html.

Consider [COPYING](COPYING) and [COPYING.LGPL](COPYING.LGPL).


## Acknowledgement
warc2graph makes heavy and critical use of following open source libraries:

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [matplotlib](https://matplotlib.org/)
* [NetworkX](https://networkx.org/)
* [Selenium](https://www.selenium.dev/)
* [Setuptools](https://setuptools.readthedocs.io/en/latest/)
* [Warcio](https://github.com/webrecorder/warcio)
* [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)
* [trafilatura](https://trafilatura.readthedocs.io/en/latest/)