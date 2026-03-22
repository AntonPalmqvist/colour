
import colour
from colour.utilities import message_box
import numpy as np
from pprint import pprint
import math

xy = [0.343211370103531, 0.360207541805137] # Standard observer 2 degree CIE 1931
XYZ = colour.xy_to_XYZ(xy)
CAT = "Bradford"
illuminant = colour.RGB_COLOURSPACES["sRGB"].whitepoint # Illuminant of the input CIE XYZ tristimulus values

def distance_to_planckian_locus(xy):

    # Calculates distance from the Planckian locus, "Duv" https://www.waveformlighting.com/tech/calculate-duv-from-cie-1931-xy-coordinates
    u = (4*xy[0]) / (-2*xy[0] + 12*xy[1] + 3)
    v = (6*xy[1]) / (-2*xy[0] + 12*xy[1] + 3)
    k6 =-0.00616793
    k5 =0.0893944
    k4 =-0.5179722
    k3 =1.5317403
    k2 =-2.4243787
    k1 =1.925865
    k0 =-0.471106
    Lfp = math.sqrt(math.pow((u - 0.292),2)+math.pow((v-0.24),2))
    a = math.acos((u-0.292)/Lfp)
    Lbb = k6*math.pow(a,6) + k5*math.pow(a,5) + k4*math.pow(a,4) + k3*math.pow(a,3) + k2*math.pow(a,2) + k1*a+k0
    Duv = Lfp - Lbb

    return round(Duv,4)

def round_decimals(value):
    if isinstance(value, (list, tuple, np.ndarray)):
        return [round_decimals(x) for x in value]
    return float(f"{value:.3f}")

distance = distance_to_planckian_locus(xy)

message_box(f"")

message_box(f"CIE xy: {xy}\nCIE XYZ: {round_decimals(XYZ)}")

sRGB = round_decimals(colour.convert(xy, 'CIE xy', 'sRGB'))
sRGBLinear = round_decimals(colour.XYZ_to_RGB(XYZ, 'sRGB', illuminant, CAT))
message_box(f"sRGB: {sRGB}\nsRGB Linear: {sRGBLinear}\nsRGB Linear (Normalized): {round_decimals(colour.algebra.normalise_maximum(sRGBLinear))}")

ACES = round_decimals(colour.XYZ_to_RGB(XYZ, 'ACEScg', illuminant, CAT))
message_box(f"ACEScg: {ACES}\nACEScg (Normalized): {round_decimals(colour.algebra.normalise_maximum(ACES))}")

message_box(f"CCT: {round(colour.temperature.XYZ_to_CCT_Ohno2013(XYZ)[0])} K ({distance})" if -0.005 <= distance <= 0.005 else f"CCT: N/A ({distance})")

# pprint(sorted(colour.RGB_COLOURSPACES.keys()))

message_box(f"")

colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(["D50", "D55" ,"D65", "D75", "E", {"Custom": np.array([xy[0], xy[1]])}])