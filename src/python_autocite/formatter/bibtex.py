from python_autocite.formatter import CitationFormatter


class BibTexFormatter(CitationFormatter):

    def format(self, citation):

        if citation.publication_date is not None:
            format_str = "@misc{%s, title={%s}, url={%s}, year={%s}, month={%s}, author={%s} }"
            return format_str % (
                citation.unique_id,
                citation.title,
                citation.url.strip(),
                citation.publication_date.year,
                citation.publication_date.month,
                self._assemble_authors(citation.authors),
                )
        else:
            format_str = "@misc{%s, title={%s}, url={%s}, author={%s} }"
            return format_str % (
                citation.unique_id,
                citation.title,
                citation.url.strip(),
                self._assemble_authors(citation.authors),
                )

    def _get_author_format(self, authors):
        if (len(authors) == 0):
            return self.AUTHOR_UNKNOWN
        elif (len(authors) == 1):
            return "%s"
        elif (len(authors) == 2):
            return "%s and %s"
        else:
            format_string = "%s and " * (len(authors)-1)
            return format_string + " %s"

    def _assemble_authors(self, authors):

        formatted_names = set()

        for a in authors:
            first_last = a.split()
            if (len(first_last) > 1):
                # This pulls the last name and first initial
                formatted_names.add(first_last[1] + ", " + first_last[0])

        authors = list(formatted_names)
        if (len(authors) < 1):
            return self.AUTHOR_UNKNOWN

        authors.sort()

        formatted_authors = self._get_author_format(authors) % tuple(authors)
        return formatted_authors

