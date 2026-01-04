
import colour
from colour.utilities import message_box
import numpy as np
from pprint import pprint

xy = [0.31270, 0.32900]
XYZ = colour.xy_to_XYZ(xy)
CAT = "Bradford"
illuminant = colour.RGB_COLOURSPACES["sRGB"].whitepoint

def distance_to_planckian_locus(xy):
    """
    Calculate the minimum distance from a given xy coordinate to the Planckian locus.

    Args:
        xy (list or array): The xy chromaticity coordinate.
        CCT_range (tuple): Range of CCT values to sample the Planckian locus.
        steps (int): Number of steps to sample the Planckian locus.

    Returns:
        float: Minimum distance to the Planckian locus.
    """
    CCTs = np.linspace(1667, 25000, 100)
    planckian_xy = np.array([colour.CCT_to_xy(CCT) for CCT in CCTs])

    # Calculate Euclidean distance to each point on the Planckian locus
    distances = np.linalg.norm(planckian_xy - xy, axis=1)

    return np.min(distances)

distance = distance_to_planckian_locus(xy)

message_box(f"")

message_box(f"XYZ: {XYZ}")

message_box(f"sRGB: {colour.convert(xy, 'CIE xy', 'sRGB')}")

sRGBLinear = colour.XYZ_to_RGB(XYZ,'sRGB', illuminant, CAT)
message_box(f"sRGB Linear: {sRGBLinear}\n"f"Normalized: {colour.algebra.normalise_maximum(sRGBLinear)}")

ACES = colour.XYZ_to_RGB(XYZ,'ACEScg', illuminant, CAT)
# message_box(f"ACEScg: {ACES}\n"f"Normalized: {colour.algebra.normalise_maximum(ACES)}") #Not correct

message_box(f"CCT: - ({distance})" if distance > 0.005 else f"CCT: {colour.xy_to_CCT(xy)} ({distance})")

# pprint(sorted(colour.RGB_COLOURSPACES.keys()))

message_box(f"")

colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(["D50", "D55" ,"D65", "D75", "E", {"Custom": np.array([xy[0], xy[1]])}])