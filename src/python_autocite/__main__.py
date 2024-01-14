#!/bin/env python3

import requests
from bs4 import BeautifulSoup
from python_autocite.lib.citation import Citation
from python_autocite.formatter.apa import APAFormatter
from python_autocite.formatter.bibtex import BibTexFormatter
from python_autocite.formatter.ieee import IEEEFormatter
from python_autocite.lib.datafinder import Datafinder
from python_autocite.lib.capture import PageCapture
import datetime
import sys
import argparse

def url_to_soup(url):
    # Some websites are unhappy with no user agent, so here's
    # one that looks nice.
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

    try:
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')
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

    parser.add_argument(
            '--capture',
            required=False,
            default=False,
            action="store_true",
            help="Capture a screenshot of the website using pageres. Requires pageres to be installed. This does not work with all websites."
            )

    parser.add_argument(
            '--non-interactive',
            required=False,
            default=False,
            action='store_true',
            help="Run non-interactively. autocite will not prompt for data and will leave placeholders in your citations."
            )

    parser.add_argument(
            '--format',
            required=False,
            default='apa',
            help="Output citation format. 'bibtex', 'apa', and 'ieee' are supported. Defaults to 'apa'."
            )

    args = parser.parse_args()
    if (len(sys.argv) < 2):
        parser.print_help()
        sys.exit(1)


    if args.format.lower() == 'apa':
        formatter = APAFormatter()
    elif args.format.lower() == 'bibtex':
        formatter = BibTexFormatter()
    elif args.format.lower() == 'ieee':
        formatter = IEEEFormatter()
    else:
        print("Unsupported/unrecognized formatter. Run autocite --help to see supported formatters.")
        sys.exit(1)

    citations = []

    if (args.url is not False):
        soup = url_to_soup(args.url)
        if (soup is not None):
            citation = soup_to_citation(args.url, soup)
            citations.append(citation)
            if args.capture is not False:
                capture = PageCapture(citation)
                capture.capture()
        else:
            print("Unable to load " + str(args.url), file=sys.stderr)

    if (args.from_file is not False):
        with open(args.from_file) as f:
            for line in f:
                print(".", end="", file=sys.stderr)
                sys.stderr.flush()
                soup = url_to_soup(line)
                if (soup is not None):
                    citation = soup_to_citation(line, soup)
                    citations.append(citation)
                    if args.capture is not False:
                        capture = PageCapture(citation)
                        capture.capture()
                else:
                    print("Unable to load " + str(line), file=sys.stderr)
            print()
            # Start a new line, split with dot(s)

    formatted_citations = []

    for citation in citations:
        formatted = formatter.format(citation)
        if not args.non_interactive:
            if("[[[AUTHORS]]]" in formatted):
                print("For URL: "+str(citation.url))
                formatted=formatted.replace("[[[AUTHORS]]]",input("Please enter author(s) manually: "))
            if("[[[PUBLICATION DATE]]]" in formatted):
                print("For URL: "+str(citation.url))
                formatted=formatted.replace("[[[PUBLICATION DATE]]]",input("Please enter publication date manually: "))
            if("[[[TITLE]]]" in formatted):
                print("For URL: "+str(citation.url))
                formatted=formatted.replace("[[[TITLE]]]",input("Please enter the title manually: "))
        formatted_citations.append(formatted)

    formatted_citations.sort()

    if (args.to_text is not False):
        with open(args.to_text, "w") as f:
            for citation in formatted_citations:
                f.write(citation)
                f.write("\n\n")
    else:
        print("Your citations:")
        print()
        for citation in formatted_citations:
            print(citation)

if __name__ == "__main__":
    main()
