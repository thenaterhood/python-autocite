from datetime import datetime
from dateutil import parser as date_parser


class Citation(object):

    __slots__ = [
            '_authors',
            '_pubdate',
            '_access_date',
            '_title',
            '_url'
            ]

    def __init__(self):
        self._authors = []

    @property
    def unique_id(self):
        '''
        Provides a unique, deterministic ID for the citation using the
        available data
        '''
        unique_id = ""

        if self._pubdate is not None:
            unique_id = str(self._pubdate.year) + '_'

        if self._title is not None and len(self._title) > 0 and self._title != "[[[TITLE]]]":
            unique_id = unique_id + ''.join([e for e in self._title if e.isalnum()])[0:15]
        elif self._url is not None and len(self._url) > 0:
            unique_id = unique_id + ''.join([e for e in self._url if e.isalnum()])[0:15]

        return unique_id

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, author):
        if (type(author) is list):
            self._authors += author
        else:
            self._authors.append(author)

    @authors.deleter
    def authors(self):
        self._authors = []

    @property
    def publication_date(self):
        return self._pubdate

    @publication_date.setter
    def publication_date(self, value):
        self._pubdate = self._handle_date(value)

    @property
    def access_date(self):
        return self._access_date

    @access_date.setter
    def access_date(self, value):
        self._access_date = self._handle_date(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def _handle_date(self, value):
        if (isinstance(value, datetime)):
            return value
        else:
            try:
                return date_parser.parse(value)
            except:
                return None

