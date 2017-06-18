python-autocite
============

python-autocite provides modules and a command line utility
for automatically generating citiations of web pages.

Licensed under the MIT license. Though not required by the
license, please consider dropping a line if you find this
software useful.

Installation
------------

Requirements:

* BeautifulSoup4
* Requests
* Dateutil
* Python 3

Run `python setup.py install` to install.

Usage
-----------
Command line usage:

Run `autocite --help` to see the help text.

Protip: Missing information will be filled in with "[[[field name]]]" which should make it easy to search for.

Using in other programs:

`from python_autocite.lib import *`

The modules available are:
* `python_autocite.lib.datafinder.Datafinder` - attempts to pull
publication information from a BeautifulSoup soup
* `python_autocite.lib.citation.Citation` - Contains citation data, 
with intelligent setters
* `python_autocite.lib.formatter.CitationFormatter` - Interface for
creating citation formatters
* `python_autocite.lib.formatter.APAFormatter` - formats a Citation
into an APA citation

Examples
-----------

Cite a single URL:

`autocite --url http://arstechnica.com/business/2012/12/report-data-caps-just-a-cash-cow-for-internet-providers/`

This will print to stdout:

`Anderson, N. (2012, December 18). Report: data caps just a “cash cow” for Internet providers. Retrieved June 18, 2017, from http://arstechnica.com/business/2012/12/report-data-caps-just-a-cash-cow-for-internet-providers/`

Cite a list of URLs (newline separated), and save the citations to a file called citations.txt

`autocite --from-file urllist.txt --to-text citations.txt`

Disclaimers
-----------
This software is not perfect and will make mistakes. Check that
your citations are correct before using them for any important
purpose.

