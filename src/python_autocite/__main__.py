#!/bin/env python3

import requests
from bs4 import BeautifulSoup
from python_autocite.lib.citation import Citation
from python_autocite.lib.formatter import APAFormatter
from python_autocite.lib.datafinder import Datafinder
import datetime
import sys
import argparse

def url_to_soup(url):
    # Some websites are unhappy with no user agent, so here's
    # one that looks nice.
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

    try:
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html5lib')
    except Exception as e:
        print(e)
        return None

def soup_to_citation(url, soup):
    df = Datafinder(soup)

    citation = Citation()
    citation.authors = df.get_authors()
    citation.title = df.get_title()
    citation.access_date = datetime.datetime.now()
    citation.publication_date = df.get_publication_date()
    citation.url = url
    return citation

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--url',
            required=False,
            default=False,
            help="A URL of a webpage to cite."
            )

    parser.add_argument(
            '--from-file',
            required=False,
            default=False,
            help="A file of URLs to generate citations for."
            )

    parser.add_argument(
            '--to-text',
            required=False,
            default=False,
            help="A file to write citations to. If not specified, citations will be written to stdout."
            )

    args = parser.parse_args()
    if (len(sys.argv) < 2):
        parser.print_help()
        sys.exit(1)


    formatter = APAFormatter()
    citations = []

    if (args.url is not False):
        soup = url_to_soup(args.url)
        if (soup is not None):
            citations.append(soup_to_citation(args.url, soup))
        else:
            print("Unable to load " + str(args.url), file=sys.stderr)

    if (args.from_file is not False):
        with open(args.from_file) as f:
            for line in f:
                print(".", end="", file=sys.stderr)
                sys.stderr.flush()
                soup = url_to_soup(line)
                if (soup is not None):
                    citations.append(soup_to_citation(line, soup))
                else:
                    print("Unable to load " + str(args.url), file=sys.stderr)

    formatted_citations = []
    for citation in citations:
        formatted_citations.append(formatter.format(citation))

    formatted_citations.sort()
    if (args.to_text is not False):
        with open(args.to_text, "w") as f:
            for citation in formatted_citations:
                f.write(citation)
                f.write("\n\n")
    else:
        for citation in formatted_citations:
            tmp=str(citation)
            if("[[[AUTHORS]]]" in tmp):
                tmp=tmp.replace("[[[AUTHORS]]]",input("Please enter author(s) manually: "))
            if("[[[PUBLICATION DATE]]]" in tmp):
                tmp=tmp.replace("[[[PUBLICATION DATE]]]",input("Please enter publication date manually: "))
            if("[[[TITLE]]]" in tmp): #可以优化速度 yong tmp 也不行
                tmp=tmp.replace("[[[TITLE]]]",input("Please enter the title manually: "))#Forget the "=" python
            print(tmp)#missing

if __name__ == "__main__":
    main()
