from htmlentitydefs import entitydefs
from HTMLParser import HTMLParser
from collections import defaultdict
from sgmllib import SGMLParser  
import sys, urllib2
import conf

class GplusParser2(SGMLParser):
    def __init__(self):
        self.post_all = []
        self.post_attr = []
        self.attr_end = True
        self.post = None
        SGMLParser.__init__(self)
    
    def start_div(self, attrs):
        #post start
        if self.attrs_value(attrs, "class") == "Tg Sb":
            self.post = defaultdict(str)
            self.post_all.append(self.post)

        #post id start 
        if self.attrs_value(attrs, "class") == "Tg Sb":
            self.post["id"] = self.attrs_value(attrs, "id")

        #post text start
        if self.attrs_value(attrs, "class") == "wm VC Dq2JMd":
            self.post_attr.append("text")

        #post +1 start
        if self.attrs_value(attrs, "class") == "G8 ol le":
            self.post_attr.append( "plus")

        #post forward
        if self.attrs_value(attrs, "class") == "eK":
            self.post_attr.append("forward")
        if self.attrs_value(attrs, "class") == "Jw":
            self.post_attr.append("forward_inner")

    def start_img(self,attrs):
        if self.attrs_value(attrs, "class") == "ev aG":
            self.post["image"] = self.attrs_value(attrs, "src")

    def start_span(self, attrs):
        if self.attrs_value(attrs, "class") == "gh Ni":
            self.post_attr.append("comments")

    def handle_data(self, text):
        if len(self.post_attr) > 0:
            self.post[self.post_attr[-1]] += text

    def end_div(self):
        if len(self.post_attr) > 0:
            self.post_attr.pop()

    def end_span(self):
        if len(self.post_attr) > 0:
            self.post_attr.pop()
        

    def attrs_value(self, attrs, key):
        for attr in attrs:
            if attr[0] == key:
                return attr[1]
        return None

class GplusParser(HTMLParser):
    def __init__(self):
        self.post_all = []
        self.post_attr = []
        self.attr_end = True
        self.post = None
        HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        #post start
        if tag == "div" and self.attrs_value(attrs, "class") == "Tg Sb":
            self.post = defaultdict(str)
            self.post_all.append(self.post)

        #post id start 
        if tag == "div" and self.attrs_value(attrs, "class") == "Tg Sb":
            self.post["id"] = self.attrs_value(attrs, "id")

        #post image start
        if tag == "img" and self.attrs_value(attrs, "class") == "ev aG":
            self.post["image"] = self.attrs_value(attrs, "src")

        #post text start
        if tag == "div" and self.attrs_value(attrs, "class") == "wm VC Dq2JMd":
            self.post_attr.append("text")

        #post comments start
        if tag == "span" and self.attrs_value(attrs, "class") == "gh Ni":
            self.post_attr.append("comments")

        #post +1 start
        if tag == "div" and self.attrs_value(attrs, "class") == "G8 ol le":
            self.post_attr.append( "plus")

        #post forward
        if tag == "div" and self.attrs_value(attrs, "class") == "eK":
            self.post_attr.append("forward")
        if tag == "div" and self.attrs_value(attrs, "class") == "Jw":
            self.post_attr.append("forward_inner")

    def handle_data(self, data):
        if len(self.post_attr) > 0:
            self.post[self.post_attr[-1]] += data

    def handle_endtag(self, tag):
        if tag != "div" and self.post_attr == "text":
            return
        if len(self.post_attr) > 0:
            self.post_attr.pop()

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name])
        else:
            self.handle_data("&" + name + ";")

    def attrs_value(self, attrs, key):
        for attr in attrs:
            if attr[0] == key:
                return attr[1]
        return None

def gplus_post():
    posts = []
    for url in conf.GPLUS_URLS:
        #html = urllib2.urlopen(url=url, timeout = 30).read()
        html = open("format.html", "r").read()
        #print html
        #open("format.html", "w").write(html)
        
        gp = GplusParser2()
        gp.feed(html)
        print "post number:", len(gp.post_all)
        posts += gp.post_all

    return posts


if __name__ == '__main__':
    posts = gplus_post()
    
    for post in posts:
        fd = sys.stdout
        for k, v in post.items():
            fd.write(k + ":\n")
            fd.write(v)
            fd.write("\n\n")
