import subprocess
import sys


class PageCapture():

    def __init__(self, url):
        self._url = url

    def capture(self):
        filename = self._url.replace(".", "_").replace("/", "-")
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ' or c == '_' or c == '-']).rstrip()
        try:
            subprocess.check_output(['pageres', self._url, '--filename', filename], timeout=10)
        except:
            print("Failed to capture %s. Make sure the pageres utility is available. This does not work with all websites." % (self._url,), file=sys.stderr)

