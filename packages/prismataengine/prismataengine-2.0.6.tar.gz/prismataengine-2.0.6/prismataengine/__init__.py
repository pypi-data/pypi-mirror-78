from _prismataengine import *
import importlib_resources
with importlib_resources.path(__name__, 'cardLibrary.jso') as path:
    init(str(path))
