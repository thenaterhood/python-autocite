import subprocess
import sys


class PageCapture():

    def __init__(self, citation):
        self._citation = citation

    def capture(self):
        url = self._citation.url
        pubdate = self._citation.publication_date
        title = self._citation.title

        filename = ""

        if pubdate is not None:
            filename = self._citation.publication_date.strftime("%Y-%m-%d")

        if len(filename) > 0:
            filename = filename + " "

        if self._citation.title is not None and self._citation.title != "[[TITLE]]":
            filename = filename + self._citation.title
        else:
            filename = filename + self._citation.url


        filename = filename.replace(".", "_").replace("/", "-")
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ' or c == '_' or c == '-']).rstrip()
        try:
            subprocess.check_output(['pageres', self._citation.url, '--filename', filename], timeout=10)
        except Exception as e:
            print("Failed to capture %s. Make sure the pageres utility is available. This does not work with all websites." % (self._citation.url,), file=sys.stderr)

