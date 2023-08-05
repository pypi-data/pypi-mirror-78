"""
A basic scraper to collect paths from Maya and some common plugins according to a whitelist.


"""

import os
import re

import pymel.core as pm
import maya.api.OpenMaya as om


IMAGE_EXT_REGEX = re.compile(
    r"^\.(jpg|jpeg|gif|iff|psd|png|pic|tga|tif|tiff|bmp|hdr)$", re.IGNORECASE)

# Order MATTERS. Put the most specific expressions first.
tokens = (
    r"#+"  # image.####.exr - hash
    , r"_MAPID_"  # image_MAPID_.exr - mapid
    , r"%0\d+d"  # image.%04d.exr - percent
    , r"<UDIM>"  # image.<UDIM>.exr - udim_mari
    , r"<UVTILE>"  # image.<UVTILE>.exr - udim_mudbox
    , r"\$\d*U.*\$\d*V"  # image.u$2U_v$2V.exr or image.u$Uv$V.exr, etc - udim_vray
    , r"u<U>_v<V>"  # image.u<U>_v<V>.exr - udim_zbrush
    , r"u<U>_v<V>_<f>"  # image.u<U>_v<V>_<f>.exr - udim_zbrush_f
    , r"<[fF]\d*>"  # image.<f>.exr - frame_seq
    , r"<Frame>"  # image.<Frame>.ext - Redshift
)


TOKEN_RX = re.compile("|".join(tokens), re.IGNORECASE)

ATTRS = {
    "exampleGroup": {
        "someNodeType": ["topLevelAttribute", "nestedAttribute", "arrayTypeAttribute", "childOfNestedArrayTypeAttribute"]
    },
    "mtoa":
    {
        "aiImage": ["filename"],
        "aiPhotometricLight":  ["aiFilename"],
        "aiStandIn": ["dso"],
        "aiVolume": ["dso", "filename"],
        "mesh": ["dso"]
    },
    "AbcImport": {
        "AlembicNode": ["abc_File"]
    },
    "MayaBuiltin": {
        "file": ["computedFileTextureNamePattern"],
        "cacheFile": ["cachePath"],
        "gpuCache": ["cacheFileName"]
    },
    "yeti": {
        "pgYetiMaya": [
            "cacheFileName",
            "imageSearchPath",
            "outputCacheFileName"
        ]
    },
    "Renderman_for_Maya": {
        "PxrBump": [
            "filename"
        ],
        "PxrCookieLightFilter": [
            "map"
        ],
        "PxrDiskLight": [
            "iesProfile"
        ],

        "PxrDomeLight": [
            "lightColorMap"
        ],

        "PxrGobo": [
            "map"
        ],
        "PxrGoboLightFilter": [
            "map"
        ],

        "PxrLayeredTexture": [
            "maskTexture",
            "filename"
        ],

        "PxrMultiTexture": [
            "filename0",
            "filename1",
            "filename2",
            "filename3",
            "filename4",
            "filename5",
            "filename6",
            "filename7",
            "filename8",
            "filename9",
        ],
        "PxrNormalMap": [
            "filename"
        ],
        "PxrOSL": [
            "shadername"
        ],

        "PxrProjectionLayer": [
            "channelsFilenames",
            "filename"
        ],
        "PxrPtexture": [
            "filename"
        ],

        "PxrRectLight": [
            "lightColorMap",
            "iesProfile"
        ],

        "PxrSphereLight": [
            "iesProfile"
        ],
        "PxrStdAreaLight": [
            "profileMap",
            "rman__EmissionMap",
            "iesProfile",
            "barnDoorMap"
        ],

        "PxrStdEnvMapLight": [
            "rman__EnvMap"
        ],
        "PxrTexture": [
            "filename"
        ],
        "PxrVisualizer": [
            "matCap"
        ],
        "RenderManArchive": [
            "filename"
        ],
        "rmanImageFile": [
            "File"
        ],
        "rmanTexture3d": [
            "File"
        ],
        "RMSAreaLight": [
            "mapname"
        ],
        "RMSCausticLight": [
            "causticPhotonMap"
        ],
        "RMSEnvLight": [
            "rman__EnvMap"
        ],
        "RMSGPSurface": [
            "SpecularMapB",
            "SpecularMap",
            "RoughnessMap",
            "MaskMap",
            "SurfaceMap",
            "DisplacementMap"
        ],
        "RMSGeoAreaLight": [
            "profilemap",
            "iesprofile",
            "lightcolormap",
            "barnDoorMap"
        ],
        "RMSGeoLightBlocker": [
            "Map"
        ],
        "RMSGlass": [
            "roughnessMap",
            "surfaceMap",
            "specularMap",
            "displacementMap"
        ],
        "RMSLightBlocker": [
            "Map"
        ],
        "RMSMatte": [
            "SurfaceMap",
            "MaskMap",
            "DisplacementMap"
        ],

        "RMSOcean": [
            "roughnessMap",
            "surfaceMap",
            "specularMap",
            "displacementMap"
        ]
    },
    "vray": {
        "VRayMesh": [
            "fileName"
        ],
        "VRaySettingsNode": [
            "ifile",
            "fnm"
        ],
        "VRayVolumeGrid": [
            "inFile",
            "inPath",
        ],
        "VRayScene": [
            "FilePath"
        ]
    },
    "redshift4Maya": {
        "RedshiftBokeh": [
            "dofBokehImage"
        ],
        "RedshiftCameraMap":
        [
            "tex0"],
        "RedshiftDomeLight":
        [
            "tex0",
            "tex1"
        ],
        "RedshiftEnvironment": [
            "tex0",
            "tex1",
            "tex2",
            "tex3",
            "tex4"
        ],

        "RedshiftIESLight":
        [
            "profile"
        ],
        "RedshiftLensDistortion":
        [
            "LDimage"
        ],
        "RedshiftLightGobo":
        [
            "tex0"
        ],
        "RedshiftNormalMap":
        [
            "tex0"
        ],
        "RedshiftOptions": [
            "irradianceCacheFilename",
            "irradiancePointCloudFilename",
            "photonFilename",
            "subsurfaceScatteringFilename"
        ],
        "RedshiftPostEffects": [
            "clrMgmtOcioFilename",
            "lutFilename"
        ],
        "RedshiftProxyMesh":
        [
            "computedFileNamePattern"
        ],
        "RedshiftSprite":
        [
            "tex0"
        ],
        "RedshiftVolumeShape": [
            "computedFileNamePattern"
        ]
    }
}


ALL_NODE_TYPES = pm.allNodeTypes()


def run(_):
    """
    Find path values in attributes.

    Return a list of file paths that can be passed to a PathList.

    Use the above whitelist
    Image file textures may have a sibling ".tx file".
    """
    result = []

    plug_list = _get_plugs()
    plug_iter = om.MItSelectionList(plug_list)
    while not plug_iter.isDone():
        plug = plug_iter.getPlug()
        plug_iter.next()

        if plug.isArray:
            for index in xrange(plug.numElements()):
                child_plug = plug.elementByPhysicalIndex(index)
                value = _get_value(child_plug)
                if value:
                    result.append(_get_value(child_plug))
        else:
            value = _get_value(plug)
            if value:
                result.append(_get_value(plug))
    result = _replace_tokens(result)
    result = _expand_workspace(result)
    result = _extend_with_tx_paths(result)
    return result


def _get_value(plug):
    value = plug.asString()
    if value:
        return {"path": value, "plug": plug.name()}


def _get_plugs():
    selection_list = om.MSelectionList()
    for section in ATTRS:
        for nodetype in ATTRS[section]:
            if nodetype in ALL_NODE_TYPES:
                for node in pm.ls(type=nodetype):
                    for attr in ATTRS[section][nodetype]:
                        try:
                            selection_list.add(
                                node.attr(attr).name().replace("[-1]", "[*]"))
                        except (RuntimeError, pm.MayaAttributeError):
                            pass
    return selection_list


def _replace_tokens(paths):
    for p in paths:
        p["path"] = TOKEN_RX.sub("*", p["path"])
    return paths


def _expand_workspace(paths):
    ws = pm.Workspace()
    for p in paths:
        p["path"] = ws.expandName(p["path"])
    return paths


def _extend_with_tx_paths(paths):
    """
    Add the tx equivalent of image files

    Use glob notation for the extension (.[t][x]) because when paths are finally
    resolved, the list is expanded by globbing. 

    As TX files are not critical, we don't want to block the submission if they
    don't exist. Glob will ultimately  expand to no files if the file does not
    exist.
    """
    txpaths = []
    for p in paths:
        root, ext = os.path.splitext(p["path"])
        if IMAGE_EXT_REGEX.match(ext):
            txpath = "{}.[t][x]".format(root)
            txpaths.append({"plug": p["plug"], "path": txpath})
    return paths+txpaths
