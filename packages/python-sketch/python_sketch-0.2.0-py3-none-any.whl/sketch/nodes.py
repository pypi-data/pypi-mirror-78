import re

FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
ALL_CAPS = re.compile('([a-z0-9])([A-Z])')


def camel2snake(text):
    return ALL_CAPS.sub(r'\1_\2', FIRST_CAP.sub(r'\1_\2', text)).lower()


class SketchNode(object):
    """A base class for objects in a Sketch file"""
    def __init__(self, properties):
        """Create a node, and set the properties on the node"""
        for key, value in properties.items():
            if isinstance(value, dict) and value.get("_class"):
                value = SketchNode(value)
            elif isinstance(value, list):
                new_value = []
                for item in value:
                    if isinstance(item, dict) and item.get("_class"):
                        item = SketchNode(item)
                    new_value.append(item)
                value = new_value
            setattr(self, camel2snake(key), value)
