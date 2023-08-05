
"""
A scraper to return paths to maya files.

"""
import pymel.core as pm


def run(_):
    result = [{"path": unicode(p)} for p in pm.listReferences(recursive=True)]
    scene_name =  unicode(pm.sceneName())
    if scene_name:
        result.append({"path": scene_name})
    return result
