import feedparser
import json
from HTMLParser import HTMLParser
from pprint import pprint
from lxml import etree

def write_to_file():
    python_wiki_rss_url = "http://www.python.org/cgi-bin/moinmoin/RecentChanges?action=rss_rc"
    feed = feedparser.parse( python_wiki_rss_url)
    html = feed['feed']['summary']
    content = html.encode('latin1')

    content = "<html><body>\n" + content + "\n</body></html>"
    # print content
    with open("outfile.html", "w") as file:
        file.write(content)

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

"""
source:
http://www.xavierdupre.fr/blog/2013-10-27_nojs.html
"""
class MyHTMLParser(HTMLParser):
    def __init__(self, raise_exception=True) :
        HTMLParser.__init__(self)
        self.doc  = { }
        self.path = []
        self.cur  = self.doc
        self.line = 0
        self.raise_exception = raise_exception

    @property
    def json(self):
        return self.doc

    @staticmethod
    def to_json(content, raise_exception = False):
        parser = MyHTMLParser(raise_exception = raise_exception)
        parser.feed(content)
        return parser.json

    def handle_starttag(self, tag, attrs):
        self.path.append(tag)
        attrs = { k:v for k,v in attrs }
        if tag in self.cur :
            if isinstance(self.cur[tag],list) :
                self.cur[tag].append(  { "__parent__": self.cur } )
                self.cur = self.cur[tag][-1]
            else :
                self.cur[tag] = [self.cur[tag]]
                self.cur[tag].append(  { "__parent__": self.cur } )
                self.cur = self.cur[tag][-1]
        else :
            self.cur[tag] = { "__parent__": self.cur }
            self.cur = self.cur[tag]

        for a,v in attrs.items():
            self.cur["#" + a] = v
        self.cur[""] = ""

    def handle_endtag(self, tag):
        if tag != self.path[-1] and self.raise_exception :
            raise Exception("html is malformed around line: {0} (it might be because of a tag <br>, <hr>, <img .. > not closed)".format(self.line))
        del self.path[-1]
        memo = self.cur
        self.cur = self.cur["__parent__"]
        self.clean(memo)

    def handle_data(self, data):
        self.line += data.count("\n")
        if "" in self.cur :
            self.cur[""] += data

    def clean(self, values):
        keys = list(values.keys())
        for k in keys:
            v = values[k]
            if isinstance(v, str) :
                #print ("clean", k,[v])
                c = v.strip(" \n\r\t")
                if c != v :
                    if len(c) > 0 :
                        values[k] = c
                    else :
                        del values[k]
        del values["__parent__"]

def main():
    with open("outfile.html") as file:
        content = file.read()
        js = MyHTMLParser.to_json(content)
        pprint(js)

def debug():

    text = '{"foo":101, "bar":-0.1}'
    print is_json(text)

if __name__ == '__main__':

    main()