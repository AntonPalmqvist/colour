import colour
from colour.utilities import message_box
import numpy as np

# Extinction coefficient data prepared with convert-refractiveindex.mjs
data = {
    390:0.0000000000, 400:0.0000000000, 410:0.0000000000, 420:0.0000000000, 430:0.0000000000, 440:0.0000000001, 450:0.0000000001, 460:0.0000000001, 470:0.0000000002, 480:0.0000000003, 490:0.0000000004, 500:0.0000000006, 510:0.0000000008, 520:0.0000000011, 530:0.0000000014, 540:0.0000000018, 550:0.0000000023, 560:0.0000000028, 570:0.0000000035, 580:0.0000000042, 590:0.0000000049, 600:0.0000000057, 610:0.0000000069, 620:0.0000000086, 630:0.0000000104, 640:0.0000000122, 650:0.0000000143, 660:0.0000000166, 670:0.0000000189, 680:0.0000000209, 690:0.0000000240, 700:0.0000000290, 710:0.0000000344, 720:0.0000000403, 730:0.0000000430, 740:0.0000000492, 750:0.0000000587, 760:0.0000000708, 770:0.0000000858, 780:0.0000001020
}

def convert_k_to_alpha(k_data):
    """
    Convert extinction coefficients (k) to absorption coefficients (alpha) for each wavelength.

    Parameters:
    - k_data: Dictionary of {wavelength_nm: extinction_coefficient}

    Returns:
    - alpha_data: Dictionary of {wavelength_nm: absorption_coefficient_cm_minus_1}
    """
    alpha_data = {}
    for wavelength_nm, k in k_data.items():
        wavelength_cm = wavelength_nm * 1e-7  # Convert nm to cm
        alpha = (4 * np.pi * k) / wavelength_cm
        alpha_data[wavelength_nm] = alpha
    return alpha_data

absorption_data = convert_k_to_alpha(data)

CAT = "Bradford"
illuminant = colour.SDS_ILLUMINANTS["D65"]
sd = colour.SpectralDistribution(data)
sd_alpha = colour.SpectralDistribution(absorption_data)

def round_decimals(value):
    if isinstance(value, (list, tuple, np.ndarray)):
        return [round_decimals(x) for x in value]
    return float(f"{value:.6f}")

XYZ = colour.sd_to_XYZ(sd, illuminant=illuminant, method="Integration")
XYZ_alpha = colour.sd_to_XYZ(sd_alpha, illuminant=illuminant, method="Integration")
sRGB = colour.XYZ_to_sRGB(XYZ / 100, apply_cctf_encoding=False)
sRGB_alpha = colour.XYZ_to_sRGB(XYZ_alpha / 100, apply_cctf_encoding=False)
ACES = colour.XYZ_to_RGB(XYZ / 100, 'ACEScg', colour.RGB_COLOURSPACES["sRGB"].whitepoint, CAT)
ACES_alpha = colour.XYZ_to_RGB(XYZ_alpha / 100, 'ACEScg', colour.RGB_COLOURSPACES["sRGB"].whitepoint, CAT)

# message_box(f"CIE XYZ (k): {XYZ}")
# message_box(f"CIE XYZ Absorption: {XYZ_alpha} cm⁻¹")

# message_box(f"sRGB Linear (k): {sRGB}")
message_box(f"sRGB Linear Absorption: {round_decimals(sRGB_alpha)} cm⁻¹")

# message_box(f"ACEScg (k): {ACES}")
message_box(f"ACEScg Absorption: {round_decimals(ACES_alpha)} cm⁻¹")