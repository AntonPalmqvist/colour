
import colour
from colour.utilities import message_box
import numpy as np
from pprint import pprint
import math

XYZ = colour.temperature.CCT_to_XYZ_Ohno2013([20000,0])
CAT = "Bradford"
illuminant = colour.RGB_COLOURSPACES["sRGB"].whitepoint # Illuminant of the input CIE XYZ tristimulus values

def round_decimals(value):
    if isinstance(value, (list, tuple, np.ndarray)):
        return [round_decimals(x) for x in value]
    return float(f"{value:.3f}")

message_box(f"")

message_box(f"CIE xy: {round_decimals(colour.XYZ_to_xy(XYZ))}\nCIE XYZ: {round_decimals(XYZ)}")

sRGB = round_decimals(colour.convert(XYZ, 'CIE XYZ', 'sRGB'))
sRGBLinear = round_decimals(colour.XYZ_to_RGB(XYZ, 'sRGB', illuminant, CAT))
message_box(f"sRGB: {sRGB}\nsRGB Linear: {sRGBLinear}\nsRGB Linear (Normalized): {round_decimals(colour.algebra.normalise_maximum(sRGBLinear))}")

ACES = round_decimals(colour.XYZ_to_RGB(XYZ, 'ACEScg', illuminant, CAT))
message_box(f"ACEScg: {ACES}\nACEScg (Normalized): {round_decimals(colour.algebra.normalise_maximum(ACES))}")


message_box(f"")