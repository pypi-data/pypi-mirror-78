import re

IGNORED_PROPERTIES = ['layers']
FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
ALL_CAPS = re.compile('([a-z0-9])([A-Z])')


def camel2snake(text):
    return ALL_CAPS.sub(r'\1_\2', FIRST_CAP.sub(r'\1_\2', text)).lower()


class SketchNode(object):
    """A base class for objects in a Sketch file"""
    def __init__(self, properties):
        """Create a node, and set the properties on the node"""
        for key, value in properties.items():
            if key in IGNORED_PROPERTIES:
                continue
            setattr(self, camel2snake(key), value)


class SketchArtboard(SketchNode):
    pass


class SketchPage(SketchNode):
    def __init__(self, properties):
        """Create a page and set the properties on the page"""
        super().__init__(properties)
        self._build_structure(self, properties)

    def _build_structure(self, parent, properties):
        parent.layers = []
        for layer in properties.get('layers', []):
            if layer['_class'] == 'artboard':
                node = SketchArtboard(layer)
            else:
                node = SketchNode(layer)
            parent.layers.append(node)
            self._build_structure(node, layer)
