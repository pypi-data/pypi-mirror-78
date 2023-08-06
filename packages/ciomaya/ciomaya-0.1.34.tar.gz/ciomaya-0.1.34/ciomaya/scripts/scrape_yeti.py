   
from ciomaya.lib import scraper_utils

"""
A scraper to collect paths from Yeti nodes.
"""


ATTRS = {
    "yeti": {
        "pgYetiMaya": [
            "cacheFileName",
            "imageSearchPath",
            "outputCacheFileName"
        ]
    }
}

def run(_):

    paths = scraper_utils.get_paths(ATTRS)
    paths = scraper_utils.starize_tokens(paths, r"#+")
    paths = scraper_utils.expand_workspace(paths)
    return paths
