"""
A scraper to collect image plane movies, stills, and sequences.
"""

import os
import re
import glob
import pymel.core as pm
from ciocore.sequence import Sequence

IMAGE_PLANE_FILENAME_REGEX = re.compile(r"^(.*)\.(\d+)\.([a-z0-9]+$)")


def run(node):
    """
    Find image_plane sequences.
    """
    result = []
    print "+" * 30
    print node
    sequence = Sequence.create(node.attr("frameSpec").get())
    print sequence
    for image_plane in pm.ls(type="imagePlane"):

        result += paths_for_image_plane(image_plane, sequence)

    return result


def paths_for_image_plane(image_plane, sequence):
    """
    image_plane type may be image (possibly sequence) texture movie

    If its a movie or sequence is off, return the path.

    For sequences,
    1. evaluate the imagePlane.frameEtension for the conductorRender node's
       range.
    2. Find the padding for the sequence on disk.
    3. Compute the filenames we need expect for the rendered range.
    4. Intersect them with those that actually exist.
    """

    ws = pm.Workspace()
    iptype = image_plane.attr("type").get()
    if iptype == 1:  # texture
        return []

    plug = image_plane.attr("imageName")
    plug_name = plug.name()
    path = ws.expandName(plug.get().strip())

    match = IMAGE_PLANE_FILENAME_REGEX.match(path)

    if iptype == 2 or (not image_plane.attr("useFrameExtension").get()) or (not match):
        return [{
                "plug": plug_name,
                "path": path
                }]
    # sequence
    root, _, ext = match.groups()

    existing = glob.glob("{}.*.{}".format(root, ext))

    if not existing:
        return []

    padding = min([len(fn.split(".")[-2]) for fn in existing])

    frame_numbers = [image_plane.attr(
        "frameExtension").get(time=f) for f in sequence]
    template = "{{}}.{{:0{}d}}.{{}}".format(padding)
    used = [template.format(root, f, ext) for f in frame_numbers]

    return [{"plug": plug_name, "path": p} for p in sorted(list(set(existing) & set(used)))]
