from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(f"handle_starttag => tag 変数は {tag}")

    def handle_data(self, data):
        print(f"handle_data => data 変数は {data}")

    def handle_endtag(self, tag):
        print(f"handle_endtag => tag 変数は {tag}")

parser = MyHTMLParser()
parser.feed('<title>Python rocks!</title>')