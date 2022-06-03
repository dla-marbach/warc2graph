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

from warc2graph import linkextraction
import unittest
from warcio.archiveiterator import ArchiveIterator

warc_path = "WEB-20210202165627638-00000-24143~clarin02~8443.warc.gz"
metadata_index = 7
this_url = "https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html"
this_html = """<!DOCTYPE html>
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
"""
gold_links_index = ["page1.html", "page2.html", "angular1.html", "jquery.html"]
gold_links_index = ["https://clarin09.ims.uni-stuttgart.de/sdc_warc/" + suffix for suffix in gold_links_index]
gold_result_index = [(link, {"tag": "a"}) for link in gold_links_index]
gold_result_by_method = ({'wmd': [('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_ang1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery2.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/',
                                   'http://www.scientificlinux.org/',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/',
                                   'http://httpd.apache.org/',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/',
                                   'https://clarin09.ims.uni-stuttgart.de/icons/apache_pb2.gif',
                                   {'tag': 'img'})],
                          'bs4': [('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_ang1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery2.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/',
                                   'http://www.scientificlinux.org/',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/',
                                   'http://httpd.apache.org/',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/',
                                   'https://clarin09.ims.uni-stuttgart.de/icons/apache_pb2.gif',
                                   {'tag': 'img'})],
                          'rep': [('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/js/angular.min.js',
                                   {'tag': 'script'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_ang1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/js/jquery-1.11.3.min.js',
                                   {'tag': 'script'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery2.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'}),
                                  ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery1.html',
                                   'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                                   {'tag': 'a'})]},
                         {})

gold_result_merged = ([('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_ang1.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery2.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery1.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/',
                        'http://www.scientificlinux.org/',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/',
                        'http://httpd.apache.org/',
                        {'tag': 'a'}),
                       ('https://clarin09.ims.uni-stuttgart.de/',
                        'https://clarin09.ims.uni-stuttgart.de/icons/apache_pb2.gif',
                        {'tag': 'img'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/js/angular.min.js',
                        {'tag': 'script'}),
                       ('https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html',
                        'https://clarin09.ims.uni-stuttgart.de/sdc_warc/js/jquery-1.11.3.min.js',
                        {'tag': 'script'})],
                      {})

all_tags = [("a", "href"),
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


class TestLinkextractionMethods(unittest.TestCase):
    maxDiff = None

    def test_wmd(self):
        with open(warc_path, "rb") as warc_file:
            ai = ArchiveIterator(warc_file)
            for i, record in enumerate(ai):
                if i == metadata_index:
                    self.assertCountEqual(linkextraction._wmd(record, blacklist=[], html_tags=all_tags),
                                          gold_result_index)
                    break

    def test_bs4(self):
        self.assertCountEqual(linkextraction._bs4(this_html, this_url, blacklist=[], html_tags=all_tags),
                              gold_result_index)

    def test_rep(self):
        browser = linkextraction._set_up_browser()
        self.assertCountEqual(linkextraction._rep(this_html, this_url, blacklist=[], browser=browser, html_tags=all_tags),
                              gold_result_index)

    def test_get_links_from_warc(self):
        methods = ["wmd", "bs4", "rep"]
        browser = linkextraction._set_up_browser()

        links, node_attribs = linkextraction._get_links_form_warc(warc_path, methods=methods, store_content=False,
                                                                  collect_metadata=False, count_tags=False,
                                                                  blacklist=[], browser=browser)
        self.assertEqual(type(links), dict)
        self.assertEqual(node_attribs, {})
        self.assertCountEqual(links, gold_result_by_method[0])

    # def test_get_links_from_live(self):
    #     methods = ["bs4", "rep"]
    #     browser = linkextraction._set_up_browser()
    #     import warnings
    #     warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
    #
    #     urls = ["https://clarin09.ims.uni-stuttgart.de/sdc_warc/index.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/page1.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/page2.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/angular1.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_ang1.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_ang2.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/jquery.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery1.html",
    #             "https://clarin09.ims.uni-stuttgart.de/sdc_warc/page_target_jquery2.html"]
    #
    #     links, node_attribs = linkextraction._get_links_from_live(urls, methods, blacklist=[], store_content=False,
    #                                                               collect_metadata=False, count_tags=False,
    #                                                               browser=browser)
    #     self.assertEqual(type(links), dict)
    #     self.assertEqual(node_attribs, {})
    #     gold_result_by_method_wo_wmd, attribs = gold_result_by_method
    #     gold_result_by_method_wo_wmd = {k: v for k, v in gold_result_by_method_wo_wmd.items() if k != "wmd"}
    #     self.assertCountEqual(links, gold_result_by_method_wo_wmd)

    def test_extract_links(self):
        links, node_attribs = linkextraction.extract_links(warc_path, store_content=False, collect_metadata=False,
                                                           count_tags=False)

        self.assertEqual(type(links), list)
        self.assertEqual(node_attribs, {})
        self.assertCountEqual(links, gold_result_merged[0])


if __name__ == "__main__":
    unittest.main()
