class CitationFormatter(object):

    AUTHOR_UNKNOWN = "[[[AUTHORS]]]"
    PUBDATE_UNKNOWN = "[[[PUBLICATION DATE]]]"
    ACCESSDATE_UNKNOWN = "[[[ACCESS DATE]]]"

    def format(citation):
        raise NotImplementedError("Citation format not implemeted")

