from python_autocite.formatter import CitationFormatter


class IEEEFormatter(CitationFormatter):

    def format(self, citation):
        # Format strings with and without publishign date
        format = "%s, \"%s,\" %s. [Online]. Available: %s."
        format_no_date = "%s, \"%s.\" [Online]. Available: %s."

        # Optional trailing format string for access date
        format_access = "[Accessed %s]"
        
        if self._format_pubdate(citation.publication_date) == self.PUBDATE_UNKNOWN:

            output = format_no_date % (
                self._assemble_authors(citation.authors),
                citation.title,
                citation.url,
                )        
        else:
            output = format % (
                self._assemble_authors(citation.authors),
                citation.title,
                self._format_pubdate(citation.publication_date),
                citation.url,
                ) 

        if self._format_accessdate(citation.access_date) == self.ACCESSDATE_UNKNOWN:
            output = output + (format_access % self._format_accessdate(citation.access_date))

        return output
    
    def _get_author_format(self, authors):
        if (len(authors) == 0):
            return self.AUTHOR_UNKNOWN
        elif (len(authors) == 1):
            return "%s"
        elif (len(authors) == 2):
            return "%s, and %s"
        elif (len(authors) > 6):
            return "%s et al."
        else:
            format_string = "%s, " * (len(authors)-1)
            return format_string + "and %s"

    def _assemble_authors(self, authors):

        formatted_names = set()

        for a in authors:
            first_last = a.split()
            if (len(first_last) > 1):
                # This pulls the last name and first initial
                formatted_names.add(first_last[0][0] + ", " + first_last[1])

        authors = list(formatted_names)
        if (len(authors) < 1):
            return self.AUTHOR_UNKNOWN

        authors.sort()
        if (len(authors) > 6):
            formatted_authors = self._get_author_format(authors) % authors[0]
        else:
            formatted_authors = self._get_author_format(authors) % tuple(authors)
            
        return formatted_authors

    def _format_pubdate(self, date):
        if (date is not None):
            return date.strftime("%Y, %B %d")
        else:
            return self.PUBDATE_UNKNOWN

    def _format_accessdate(self, date):
        if (date is not None):
            return date.strftime("%B %d, %Y")
        else:
            return self.ACCESSDATE_UNKNOWN


