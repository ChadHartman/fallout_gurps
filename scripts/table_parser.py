#!/usr/bin/env python3

from html.parser import HTMLParser


class TableParser(HTMLParser):

    def __init__(self):
        super(TableParser, self).__init__()
        self.rows = []
        self.current_item = []
        self.record_data = False
        self.in_th = False

    def __clean__(self, value):
        value = value.replace("\n", "").replace("\t", " ")

        while True:
            old_len = len(value)
            value = value.replace("  ", " ")
            if old_len == len(value):
                break

        return value.strip()

    def handle_starttag(self, tag, attrs):
        if tag == 'th':
            self.record_data = True
            self.in_th = True
        elif tag == 'td':
            self.record_data = True
        elif tag == 'tr':
            self.rows.append([])
        elif tag == "span" and self.in_th:
            capture_title = False
            title = None
            for pair in attrs:
                if pair[0] == "class" and pair[1] == "va-icon":
                    capture_title = True
                elif pair[0] == "title":
                    title = pair[1]
            if capture_title:
                if not self.rows[-1][-1]:
                    # Previously captured empty text
                    del self.rows[-1][-1]
                self.rows[-1].append(self.__clean__(title))
                self.record_data = False

    def handle_endtag(self, tag):

        if (tag == 'th' or tag == 'td') and self.record_data:
            self.rows[-1].append(" ".join(self.current_item).strip())
            self.record_data = False
            self.current_item = []

        if tag == "th":
            self.in_th = False

    def handle_data(self, data):
        if not self.record_data:
            return

        value = self.__clean__(data)
        self.current_item.append(value)


def main():

    parser = TableParser()
    with open("../assets/weapons/unarmed.html", 'r') as f:
        parser.feed("".join(f.readlines()))

    import json

    for row in parser.rows:
        # print(json.dumps(row))
        print("\t".join(row))


if __name__ == "__main__":
    main()
