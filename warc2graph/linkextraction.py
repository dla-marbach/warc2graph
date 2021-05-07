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

# file management
import os

# read warc files
from warcio.archiveiterator import ArchiveIterator
import re

# parse html
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

# remote controlled browser
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, TimeoutException
from webdriver_manager.firefox import GeckoDriverManager

# handle media
import io
import matplotlib.pyplot as plt

# misc
from warnings import warn
from collections import Counter
from collections import defaultdict
import time


implemented_methods = ["wmd", "bs4", "rep"]
# TODO allow choice for subsets
html_link_tags = [("a", "href"),
                  ("frame", "src"),
                  ("iframe", "src"),
                  ("link", "href"),
                  ("base", "href"),
                  ("object", "data"),
                  ("img", "src"),
                  ("applet", "object"),
                  ("embed", "src"),
                  ("meta", "url"),
                  ("meta", "content"),
                  ("audio", "src"),
                  ("video", "src"),
                  ("script", "src"),
                  ("area", "href"),
                  ("form", "action"),
                  ("button", "formation"),
                  ("q", "cite"),
                  ("blockquote", "cite")]


# ====================================================
def _decode_warc_html(record, prob_encoding):
    encoded_content = record.content_stream().read()
    encoding_successful = False
    html_content = ""
    cascade = ["ISO-8859-1", "ISO-8859-8", "utf-8", "utf-16"]
    if prob_encoding is not None:
        cascade.insert(0, prob_encoding)
    for encoding in cascade:
        try:
            html_content = encoded_content.decode(encoding)
            encoding_successful = True
            break
        except UnicodeDecodeError:
            continue

    if not encoding_successful:
        raise UnicodeDecodeError(f"""'{prob_encoding}', 'ISO-8859-1', 'ISO-8859-8', 'utf-8', 'utf-16'""",
                                 encoded_content, 0, len(encoded_content), "Warc entry could not be decoded.")

    return html_content


# ====================================================
def _set_up_browser(headless=True):
    opts = webdriver.firefox.options.Options()
    if headless:
        opts.headless = True
        opts.add_argument("--headless")
    import platform
    if platform.system() in ["Linux", "Darwin"]:
        log_path = "/tmp/geckodriver.log"
    else:
        log_path = "."
    os.environ["WDM_LOG_LEVEL"] = "0"
    os.environ["WDM_PRINT_FIRST_LINE"] = "False"
    exec_path = GeckoDriverManager(cache_valid_range=30, log_level=0, print_first_line=False).install()
    browser = webdriver.Firefox(executable_path=exec_path, options=opts, service_log_path=log_path)
    return browser


# ====================================================
def _get_url_from_meta(content):
    if content is None:
        return None
    content_attribs = content.split(";")
    li = None
    for c_attrib in content_attribs:
        if "url" in c_attrib:
            li = c_attrib.split("=")[1].strip()
            break
    return li


# ====================================================
def _wmd(record, blacklist) -> list:
    wanted = [w[0] + "/@" + w[1] for w in html_link_tags]
    content = record.content_stream().read().decode("utf-8")

    found_links = []
    for target, typ in re.findall(r"outlink: (.*?) [A-Z] (.*)\b", content):
        if typ in wanted and "robots.txt" not in target and "mailto" not in target and urlparse(
                target).netloc not in blacklist:
            found_links.append((target, {"tag": typ.split("/")[0]}))
    return found_links


# ====================================================
def _bs4(html, this_url, blacklist):
    found_links = []
    soup = BeautifulSoup(html, "html.parser")
    # TODO parse javascript

    for tag, attr in html_link_tags:
        links = soup.findAll(tag)
        for link in links:
            content = link.get(attr)

            if tag == "meta" and attr == "content":
                url = _get_url_from_meta(content)
                if url is None:
                    continue
            else:
                url = urlparse(content)

            if url.geturl() == b"":  # happens when there is no href or src attribute
                continue
            elif url.scheme in ["http", "https"]:
                if url.netloc not in blacklist:
                    target = url.geturl()
                else:
                    continue
            elif url.netloc == "":
                target = urljoin(this_url, url.path)
            else:
                continue
            # save the found connection and its type
            if "robots.txt" not in target and "mailto" not in target:
                found_links.append((target, {"tag": tag}))

    return found_links


# ====================================================
def _rep(html, this_url, blacklist, browser):
    found_links = []

    cwd = os.getcwd()
    tmp_file_name = ".tmp.html"

    rep_success = None
    while rep_success is None:
        tmp_path = os.path.join(cwd, tmp_file_name)
        with open(tmp_path, "w") as tmp:
            tmp.write(html)

        try:
            browser.get(f"file://{tmp_path}")
            time.sleep(.5)
            rep_success = True
            if "<script" in html:
                time.sleep(2.5)
        except (WebDriverException, TimeoutException) as _:
            rep_success = False
        except NoSuchWindowException:
            browser = _set_up_browser()
        except Exception as e:
            raise e
        finally:
            os.remove(tmp_path)

    for tag, attr in html_link_tags:
        if rep_success:
            # using selenium
            try:
                found_links_here = browser.find_elements_by_xpath(f"//{tag}[@{attr}]")
                # TODO check if this really examines dom and not html
            except Exception as e:
                print(e)
                continue

            # clean up links
            for link in found_links_here:
                content = link.get_attribute(attr)

                # get data from content attribute in meta tag
                if tag == "meta" and attr == "content":
                    content = _get_url_from_meta(content)
                    if content is None:
                        continue

                # remove absolute path from file system
                url = os.path.relpath(urlparse(content).path, cwd)
                url = urlparse(url)

                # add original absolute path
                if url.scheme in ["http", "https"]:
                    if url.netloc not in blacklist:
                        target = url.geturl()
                elif url.netloc == "":
                    target = urljoin(this_url, url.path)
                else:
                    continue

                # save
                if "robots.txt" not in target and "mailto" not in target:
                    found_links.append((target, {"tag": tag}))

    return found_links


# ====================================================
def _do_count_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    all_tags = []
    for tag in soup.findAll():
        all_tags.append(tag.name)
    return dict(Counter(all_tags))


# ====================================================
def _get_links_form_warc(warc_path, methods, blacklist, include_content, count_tags, browser=None,
                         max_records=None):
    # data structures
    links = {m: [] for m in methods}
    node_attribs = defaultdict(dict)

    if "rep" in methods and browser is None:
        browser = _set_up_browser()

    # iterate over entries in warc file
    with open(warc_path, "rb") as warc_file:
        record_count = 0
        for record in ArchiveIterator(warc_file):
            record_count += 1

            # print(f"\r{record_count} records analyzed.", end="")

            if max_records is not None and record_count > max_records:
                raise RuntimeError(f"More records than allowed -> max_records == {max_records}")

            # get url of page
            this_url = record.rec_headers.get_header("WARC-Target-URI")
            if urlparse(this_url).netloc in blacklist or this_url is None or any(
                    [test in this_url for test in ["robots.txt", "dns:"]]):  # ignore if blacklisted
                continue

            response_record_needed = "rep" in methods or "bs4" in methods or include_content or count_tags
            # get outlinks from metadata
            if record.rec_type == "metadata" and "wmd" in methods:
                out_links = _wmd(record, blacklist)
                complete_links = [(this_url, *ol) for ol in out_links]
                links["wmd"] += complete_links

            elif record.rec_type == "resource" and include_content:
                media_check = any([m in content_type for m in ["audio", "image", "text", "video"]])
                if media_check and include_content:
                    node_attribs[this_url]["content"] = record.content_stream().read()

            # get links from parsed html using bs4 and from warc replay using selenium
            elif record.rec_type == "response" and response_record_needed:
                content_type = None
                media_check = False
                try:
                    content_type = record.http_headers.get_header("Content-Type")
                    content_check = "text/html" in content_type
                    if not content_check:
                        media_check = any([m in content_type for m in ["audio", "image", "text", "video"]])
                except (AttributeError, TypeError):
                    warn(f"Error occurred while reading warc-header in '{warc_path}'")
                    # if Content-Type is not specified in header have good faith and hope for the best
                    content_check = True

                # store media content
                if media_check and include_content:
                    binary_content = record.content_stream().read()
                    suffix = this_url.split(".")[-1].lower()
                    is_image = suffix in ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "tif"]

                    # store images as numpy array
                    if is_image:
                        stream = io.BytesIO(binary_content)
                        ready_content = plt.imread(stream, format=suffix)

                    # TODO define pythonic data types for more media types

                    # store everything that is not defined as binary data
                    else:
                        ready_content = binary_content

                    node_attribs[this_url]["content"] = ready_content

                elif content_check:
                    encoding = None
                    if content_type is None:
                        encoding = None
                    elif "=" in content_type:
                        encoding = content_type.split("=")[1]
                    html_content = _decode_warc_html(record, encoding)

                    if include_content:
                        node_attribs[this_url]["content"] = html_content

                    if count_tags:
                        node_attribs[this_url]["counted_tags"] = _do_count_tags(html_content)

                    if "rep" in methods:
                        out_links = _rep(html_content, this_url, blacklist, browser)
                        complete_links = [(this_url, *ol) for ol in out_links]
                        links["rep"] += complete_links

                    if "bs4" in methods:
                        out_links = _bs4(html_content, this_url, blacklist)
                        complete_links = [(this_url, *ol) for ol in out_links]
                        links["bs4"] += complete_links

    node_attribs = dict(node_attribs)
    return links, node_attribs


# ====================================================
def _get_links_from_live(urls, methods, blacklist, include_content, count_tags, browser=None):

    # data structures
    links = {m: [] for m in methods}
    node_attribs = defaultdict(dict)

    if "rep" in methods and browser is None:
        browser = _set_up_browser()

    for this_url in urls:
        html_content = urlopen(this_url, timeout=15.).read().decode()

        if include_content:
            node_attribs[this_url]["content"] = html_content

        if count_tags:
            node_attribs[this_url]["counted_tags"] = _do_count_tags(html_content)

        if "rep" in methods:
            out_links = _rep(html_content, this_url, blacklist, browser)
            complete_links = [(this_url, *ol) for ol in out_links]
            links["rep"] += complete_links

        if "bs4" in methods:
            out_links = _bs4(html_content, this_url, blacklist)
            complete_links = [(this_url, *ol) for ol in out_links]
            links["bs4"] += complete_links

    node_attribs = dict(node_attribs)
    return links, node_attribs


# ====================================================
def extract_links(input_data, input_type="warc", methods="all", merge_results=True, blacklist=None,
                  include_content=False, count_tags=False) -> list or dict:
    """Method to extract links from (archived) website.
    
    Parameters
    ----------
    input_data : str or list
        The data that is to be modelled. Either a path to a warc file (local or online), a list of warc files or a list
        of links to the live web.

    input_type : str, optional
        Declares the type of the input explicitly, either "warc", "download", "warc_list", or "live_list".

    methods : str or list, optional
        Which method or methods should be used for link extraction? Currently implemented: 
        "wmd", "bs4" and "rep". Also "all" is accepted and is set as default.
        If "rep" is set, Geckodriver will be installed if necessary.

    merge_results : bool, optional
        Ignored if only one method is selected. Should results of methods be merged to one result or be output as a 
        dict containing results for different methods.
    
    blacklist : list, optional
        List of domains that will be ignored.

    include_content : bool, optional
        Should the text, images and other media data be included in the model? Default: True. If include_content or
        count_tags is set, a dict containing this info will be added to the output, so the output will be a
        tuple.

    count_tags : bool, optional
        If True, all tags on every page will be counted. If include_content or count_tags is set, a dict containing
        this info will be added to the output, so the output will be a tuple.


    Returns
    -------
    tuple
        The output consists of the links and a dict containing content if include_content is set True and/or counts of
        all tags if count_tags is set True. In the case of both said flags are set False, this will be a empty
        dict. If merge_results==True or results are only generated using one method, the links will be structured as a
        list of tuples including two urls and some data describing the link. Otherwise it is structured as a dict with
        methods as keys and corresponding lists of tuples as values.
    """

    # TODO extraction of metadata for each document -> research archives unleashed

    # validating parameters
    # =====================
    if input_type not in ["warc", "download", "live_list", "warc_list"]:
        raise ValueError(f"""input_type "{input_type}" is not supported. Use either "warc" if warc_path is a local path\
        to a warc file, "download" if warc_path is a url to an online warc file, "warc_list" if warc_path is a list of\
        multiple warc files that archive one website, or "live_list" if warc_path is a list of links to the live\
        web.""")

    if methods == "all":
        methods = implemented_methods
    elif type(methods) == str:
        methods = [methods]
    elif type(methods) is not list:
        raise ValueError(f"""Use either {", ".join(implemented_methods)},
    a list containing a subset of these methods or "all" if you want to use all methods.""")

    for method in methods:
        if method not in implemented_methods + ["all"]:
            raise ValueError(f"""Method "{method}" is no known method. Use either {", ".join(implemented_methods)},
    a list containing a subset of these methods or "all" if you want to use all methods.""")

    if "wmd" in methods and input_type == "live_list":
        if len(methods) > 1:
            warn("Method wmd not available for input_type live. Only other methods will be used.")
            methods.remove("wmd")
        else:
            raise ValueError("Method wmd not available for input_type live.")

    if type(merge_results) is not bool:
        raise ValueError("merge_results must be bool.")

    if blacklist is None:
        blacklist = []
    elif type(blacklist) is not list or not all([type(u) == str for u in blacklist]):
        raise ValueError("Blacklist must be list of domains (str) that ought to be ignored.")

    if type(include_content) is not bool:
        raise ValueError("include_content must be bool.")

    if include_content and len(methods) == 1 and "wmd" in methods:
        warn("include_content is not possible if wmd is only methods. include_content will be ignored")
        include_content = False

    if count_tags and "bs4" not in methods:
        warn("count_tags is not possible without bs4. count_tags will be ignored")
        count_tags = False

    unzipped_warc = False
    if input_type == "warc" and input_data.endswith(".warc"):
        unzipped_warc = True
    elif input_type == "warc_list" and any((d.endswith(".warc") for d in input_data)):
        unzipped_warc = True
    if unzipped_warc:
        raise ValueError("You provided an unzipped warc. This program expects a zipped warc with the file extension \
                         'warc.gz'. On Linux and Mac you can zip the file(s) using 'gzip -k path/to/*.warc'.")

    # download warc
    # =============

    if input_type == "download" and type(input_data) == str and ".warc.gz" in input_data:
        warc_file = os.path.basename(input_data)
        if os.path.isfile(warc_file):
            warn(f"{warc_file} already downloaded. Will use local version.")
        else:
            remote_warc_data = urlopen(input_data).read()
            with open(warc_file, "wb") as f:
                f.write(remote_warc_data)
        input_type = "warc"
        input_data = warc_file

    # extracting links
    # ================

    browser = None
    if "rep" in methods:
        # print("Starting up wayback server and selenium browser.")
        try:
            browser = _set_up_browser()
        except (FileNotFoundError, WebDriverException):
            warn("Not able to start selenium. Probably geckodriver is not and cannot be installed. Will ignore 'rep'.")
            methods.remove("rep")
            if len(methods) == 0:
                raise ValueError("If you only want to use 'rep', geckodriver must be installed.")

    is_list_of_warcs = input_type == "warc_list" and type(input_data) == list

    if input_type == "warc" and type(input_data) == str and ".warc.gz" in input_data:
        links, node_attribs = _get_links_form_warc(input_data, methods, blacklist, include_content, count_tags,
                                                   browser=browser)

    elif is_list_of_warcs and all([type(wp) == str and ".warc.gz" in wp for wp in input_data]):
        all_links = []
        for wp in input_data:
            all_links.append(_get_links_form_warc(wp, methods, blacklist, include_content, count_tags,
                                                  browser=browser))
        links = defaultdict(list)
        node_attribs = {}
        for list_of_links, these_node_attribs in all_links:
            node_attribs.update(these_node_attribs)
            for method, these_links in list_of_links.items():
                for l in these_links:
                    if l not in links[method]:
                        links[method].append(l)

    elif input_type == "live_list" and type(input_data) == list:
        links, node_attribs = _get_links_from_live(input_data, methods, blacklist, include_content, count_tags,
                                                   browser=browser)

    else:
        raise TypeError(f"""Function create_model expects either a path a warc file if input_type=="warc", a list of \
        paths to warc files, or a list of links to the live web if input_type=="live_list". input_type was set to\
         "{input_type}", but warc_path was of type {type(input_data)}.""")

    if merge_results:
        all_links = []
        for links_of_method in links.values():
            for link in links_of_method:
                if link not in all_links:
                    all_links.append(link)
        links = all_links

    if "rep" in methods:
        browser.quit()

    return links, node_attribs
