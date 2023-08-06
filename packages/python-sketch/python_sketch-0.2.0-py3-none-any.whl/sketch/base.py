import json
import re
from zipfile import ZipFile, BadZipFile

from sketch.nodes import SketchNode

PAGE_ID = re.compile(
    r"pages/([a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}).json",
    re.IGNORECASE
)


class SketchError(Exception):
    pass


class SketchFile(object):
    """Read and parse a Sketch file"""
    pages = []

    def __init__(self, fname=None):
        """Read and parse a Sketch file"""
        if fname:
            self.open(fname)

    def open(self, fname):
        """Read and parse a Sketch file"""
        try:
            with ZipFile(fname) as zf:
                self.pages = {}
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    if info.filename in ["document.json", "meta.json", "user.json"]:
                        self._parse_object(info.filename.split('.')[0], json.loads(zf.read(info)))
                    elif info.filename.startswith('page'):
                        match = PAGE_ID.match(info.filename)
                        if not match:
                            continue
                        page_id = match.group(1)
                        self._parse_page(page_id, json.loads(zf.read(info)))
        except BadZipFile:
            raise SketchError('Not a valid Sketch file')

    def _parse_object(self, obj_type, obj):
        """Parse and create an object (document, meta, user)"""
        setattr(self, obj_type, SketchNode(obj))

    def _parse_page(self, page_id, page):
        self.pages[page_id] = SketchNode(page)
