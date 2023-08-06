"""
A basic scraper to collect paths from Maya nodes.
"""
import pymel.core as pm
from ciomaya.lib import scraper_utils


ATTRS = {
    "bifrostGraph": {
        "bifShape": ["aiFilename"]
    },
    "bifmeshio": {
        "BifMeshImportNode": ["bifMeshDirectory"]
    },
    "Boss": {
        "BossEXRInfluence": ["exrFilename"],
        "BossGeoProperties": ["cacheName", "cacheFolder"],
        "BossSpectralWave": ["velocityCacheName", "cacheName", "cacheFolder", "foamCacheName"],
        "BossWaveSolver": ["velocityCacheName", "cacheName", "foamCacheName", "cacheFolder", "remappedInputCacheName"]
    }
}

def run(_):
    """
    Find paths in Maya nodes.

    Since Maya nodes may be rendered by other renderers, and those renderers may
    support a variety of tokens, we include all tokens here. 

    Example: Renderman uses _MAPID_, but it could be found in a Maya file node. Leaky abstraction?
    Perhaps the better solution is to include the file node in the renderman scraper?

    Image file textures may have a sibling ".tx file".
    """

    paths = scraper_utils.get_paths(ATTRS)
    paths = scraper_utils.starize_tokens(paths,  r"#+" )
    paths = scraper_utils.expand_workspace(paths)

    return paths