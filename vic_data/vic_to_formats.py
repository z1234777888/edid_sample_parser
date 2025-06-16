# vic_formats.py
"""
CTA-861-I Video Format Definitions
This module defines the video format information for various VIC (Video Identification Codes)
Based on CTA-861-I specification
"""


def create_format(
    resolution: str,
    display_aspect_ratio: str,
    pixel_clock: float,
    pixel_aspect_ratio: str,
) -> dict[str, str]:
    """Create a video format dictionary with standard fields."""
    return {
        "resolution": resolution,
        "display_aspect_ratio": display_aspect_ratio,
        "pixel_clock": str(pixel_clock),
        "pixel_aspect_ratio": pixel_aspect_ratio,
    }


# Main video format definitions
video_formats = {
    # VIC 1-10
    1: create_format("640x480p @60Hz", "4:3", 25.175, "1:1"),
    2: create_format("720x480p @60Hz", "4:3", 27.0, "8:9"),
    3: create_format("720x480p @60Hz", "16:9", 27.0, "32:27"),
    4: create_format("1280x720p @60Hz", "16:9", 74.25, "1:1"),
    5: create_format("1920x1080i @60Hz", "16:9", 74.25, "1:1"),
    6: create_format("720(1440)x480i @60Hz", "4:3", 27.0, "8:9"),
    7: create_format("720(1440)x480i @60Hz", "16:9", 27.0, "32:27"),
    8: create_format("720(1440)x240p @60Hz", "4:3", 27.0, "4:9"),
    9: create_format("720(1440)x240p @60Hz", "16:9", 27.0, "16:27"),
    10: create_format("2880x480i @60Hz", "4:3", 54.0, "2:9-20:9"),
    # VIC 11-20
    11: create_format("2880x480i @60Hz", "16:9", 54.0, "8:27-80:27"),
    12: create_format("2880x240p @60Hz", "4:3", 54.0, "1:9-10:9"),
    13: create_format("2880x240p @60Hz", "16:9", 54.0, "4:27-40:27"),
    14: create_format("1440x480p @60Hz", "4:3", 54.0, "4:9, 8:9"),
    15: create_format("1440x480p @60Hz", "16:9", 54.0, "16:27, 32:27"),
    16: create_format("1920x1080p @60Hz", "16:9", 148.5, "1:1"),
    17: create_format("720x576p @50Hz", "4:3", 27.0, "16:15"),
    18: create_format("720x576p @50Hz", "16:9", 27.0, "64:45"),
    19: create_format("1280x720p @50Hz", "16:9", 74.25, "1:1"),
    20: create_format("1920x1080i @50Hz", "16:9", 74.25, "1:1"),
    # VIC 21-30
    21: create_format("720(1440)x576i @50Hz", "4:3", 27.0, "16:15"),
    22: create_format("720(1440)x576i @50Hz", "16:9", 27.0, "64:45"),
    23: create_format("720(1440)x288p @50Hz", "4:3", 27.0, "8:15"),
    24: create_format("720(1440)x288p @50Hz", "16:9", 27.0, "32:45"),
    25: create_format("2880x576i @50Hz", "4:3", 54.0, "2:15-20:15"),
    26: create_format("2880x576i @50Hz", "16:9", 54.0, "16:45-160:45"),
    27: create_format("2880x288p @50Hz", "4:3", 54.0, "1:15-10:15"),
    28: create_format("2880x288p @50Hz", "16:9", 54.0, "8:45-80:45"),
    29: create_format("1440x576p @50Hz", "4:3", 54.0, "8:15, 16:15"),
    30: create_format("1440x576p @50Hz", "16:9", 54.0, "32:45, 64:45"),
    # VIC 31-40
    31: create_format("1920x1080p @50Hz", "16:9", 148.5, "1:1"),
    32: create_format("1920x1080p @24Hz", "16:9", 74.25, "1:1"),
    33: create_format("1920x1080p @25Hz", "16:9", 74.25, "1:1"),
    34: create_format("1920x1080p @30Hz", "16:9", 74.25, "1:1"),
    35: create_format("2880x480p @60Hz", "4:3", 108.0, "2:9, 4:9, 8:9"),
    36: create_format("2880x480p @60Hz", "16:9", 108.0, "8:27, 16:27, 32:27"),
    37: create_format("2880x576p @50Hz", "4:3", 108.0, "4:15, 8:15, 16:15"),
    38: create_format("2880x576p @50Hz", "16:9", 108.0, "16:45, 32:45, 64:45"),
    39: create_format("1920x1080i(1250) @50Hz", "16:9", 72.0, "1:1"),
    40: create_format("1920x1080i @100Hz", "16:9", 148.5, "1:1"),
    # VIC 41-50
    41: create_format("1280x720p @100Hz", "16:9", 148.5, "1:1"),
    42: create_format("720x576p @100Hz", "4:3", 54.0, "16:15"),
    43: create_format("720x576p @100Hz", "16:9", 54.0, "64:45"),
    44: create_format("720(1440)x576i @100Hz", "4:3", 54.0, "16:15"),
    45: create_format("720(1440)x576i @100Hz", "16:9", 54.0, "64:45"),
    46: create_format("1920x1080i @120Hz", "16:9", 297.0, "1:1"),
    47: create_format("1280x720p @120Hz", "16:9", 148.5, "1:1"),
    48: create_format("720x480p @120Hz", "4:3", 54.0, "8:9"),
    49: create_format("720x480p @120Hz", "16:9", 54.0, "32:27"),
    50: create_format("720(1440)x480i @120Hz", "4:3", 54.0, "16:15"),
    # VIC 51-60
    51: create_format("720(1440)x480i @120Hz", "16:9", 54.0, "64:45"),
    52: create_format("720x576p @200Hz", "4:3", 108.0, "16:15"),
    53: create_format("720x576p @200Hz", "16:9", 108.0, "64:45"),
    54: create_format("720(1440)x576i @200Hz", "4:3", 108.0, "16:15"),
    55: create_format("720(1440)x576i @200Hz", "16:9", 108.0, "64:45"),
    56: create_format("720x480p @240Hz", "4:3", 108.0, "8:9"),
    57: create_format("720x480p @240Hz", "16:9", 108.0, "32:27"),
    58: create_format("720(1440)x480i @240Hz", "4:3", 108.0, "8:9"),
    59: create_format("720(1440)x480i @240Hz", "16:9", 108.0, "32:27"),
    60: create_format("1280x720p @24Hz", "16:9", 59.4, "1:1"),
    # VIC 61-70
    61: create_format("1280x720p @25Hz", "16:9", 74.25, "1:1"),
    62: create_format("1280x720p @30Hz", "16:9", 74.25, "1:1"),
    63: create_format("1920x1080p @120Hz", "16:9", 297.0, "1:1"),
    64: create_format("1920x1080p @100Hz", "16:9", 297.0, "1:1"),
    65: create_format("1280x720p @24Hz", "64:27", 59.4, "4:3"),
    66: create_format("1280x720p @25Hz", "64:27", 74.25, "4:3"),
    67: create_format("1280x720p @30Hz", "64:27", 74.25, "4:3"),
    68: create_format("1280x720p @50Hz", "64:27", 74.25, "4:3"),
    69: create_format("1280x720p @60Hz", "64:27", 74.25, "4:3"),
    70: create_format("1280x720p @100Hz", "64:27", 148.5, "4:3"),
    # VIC 71-80
    71: create_format("1280x720p @120Hz", "64:27", 148.5, "4:3"),
    72: create_format("1920x1080p @24Hz", "64:27", 74.25, "4:3"),
    73: create_format("1920x1080p @25Hz", "64:27", 74.25, "4:3"),
    74: create_format("1920x1080p @30Hz", "64:27", 74.25, "4:3"),
    75: create_format("1920x1080p @50Hz", "64:27", 148.5, "4:3"),
    76: create_format("1920x1080p @60Hz", "64:27", 148.5, "4:3"),
    77: create_format("1920x1080p @100Hz", "64:27", 297.0, "4:3"),
    78: create_format("1920x1080p @120Hz", "64:27", 297.0, "4:3"),
    79: create_format("1680x720p @24Hz", "64:27", 59.4, "64:63"),
    80: create_format("1680x720p @25Hz", "64:27", 59.4, "64:63"),
    # VIC 81-90
    81: create_format("1680x720p @30Hz", "64:27", 59.4, "64:63"),
    82: create_format("1680x720p @50Hz", "64:27", 82.5, "64:63"),
    83: create_format("1680x720p @60Hz", "64:27", 99.0, "64:63"),
    84: create_format("1680x720p @100Hz", "64:27", 165.0, "64:63"),
    85: create_format("1680x720p @120Hz", "64:27", 198.0, "64:63"),
    86: create_format("2560x1080p @24Hz", "64:27", 99.0, "1:1"),
    87: create_format("2560x1080p @25Hz", "64:27", 90.0, "1:1"),
    88: create_format("2560x1080p @30Hz", "64:27", 118.8, "1:1"),
    89: create_format("2560x1080p @50Hz", "64:27", 185.625, "1:1"),
    90: create_format("2560x1080p @60Hz", "64:27", 198.0, "1:1"),
    # Continue with higher VIC codes...
    91: create_format("2560x1080p @100Hz", "64:27", 371.25, "1:1"),
    92: create_format("2560x1080p @120Hz", "64:27", 495.0, "1:1"),
    93: create_format("3840x2160p @24Hz", "16:9", 297.0, "1:1"),
    94: create_format("3840x2160p @25Hz", "16:9", 297.0, "1:1"),
    95: create_format("3840x2160p @30Hz", "16:9", 297.0, "1:1"),
    96: create_format("3840x2160p @50Hz", "16:9", 594.0, "1:1"),
    97: create_format("3840x2160p @60Hz", "16:9", 594.0, "1:1"),
    98: create_format("4096x2160p @24Hz", "256:135", 297.0, "1:1"),
    99: create_format("4096x2160p @25Hz", "256:135", 297.0, "1:1"),
    100: create_format("4096x2160p @30Hz", "256:135", 297.0, "1:1"),
}

# 添加更高的VIC碼 (101-219) 的定義
video_formats.update(
    {
        101: create_format("4096x2160p @50Hz", "256:135", 594.0, "1:1"),
        102: create_format("4096x2160p @60Hz", "256:135", 594.0, "1:1"),
        103: create_format("3840x2160p @24Hz", "64:27", 297.0, "4:3"),
        104: create_format("3840x2160p @25Hz", "64:27", 297.0, "4:3"),
        105: create_format("3840x2160p @30Hz", "64:27", 297.0, "4:3"),
        106: create_format("3840x2160p @50Hz", "64:27", 594.0, "4:3"),
        107: create_format("3840x2160p @60Hz", "64:27", 594.0, "4:3"),
        108: create_format("1280x720p @48Hz", "16:9", 90.0, "1:1"),
        109: create_format("1280x720p @48Hz", "64:27", 90.0, "4:3"),
        110: create_format("1680x720p @48Hz", "64:27", 99.0, "64:63"),
        111: create_format("1920x1080p @48Hz", "16:9", 148.5, "1:1"),
        112: create_format("1920x1080p @48Hz", "64:27", 148.5, "4:3"),
        113: create_format("2560x1080p @48Hz", "64:27", 198.0, "1:1"),
        114: create_format("3840x2160p @48Hz", "16:9", 594.0, "1:1"),
        115: create_format("4096x2160p @48Hz", "256:135", 594.0, "1:1"),
        116: create_format("3840x2160p @48Hz", "64:27", 594.0, "4:3"),
        117: create_format("3840x2160p @100Hz", "16:9", 1188.0, "1:1"),
        118: create_format("3840x2160p @120Hz", "16:9", 1188.0, "1:1"),
        119: create_format("3840x2160p @100Hz", "64:27", 1188.0, "4:3"),
        120: create_format("3840x2160p @120Hz", "64:27", 1188.0, "4:3"),
        121: create_format("5120x2160p @24Hz", "64:27", 396.0, "1:1"),
        122: create_format("5120x2160p @25Hz", "64:27", 396.0, "1:1"),
        123: create_format("5120x2160p @30Hz", "64:27", 396.0, "1:1"),
        124: create_format("5120x2160p @48Hz", "64:27", 742.5, "1:1"),
        125: create_format("5120x2160p @50Hz", "64:27", 742.5, "1:1"),
        126: create_format("5120x2160p @60Hz", "64:27", 742.5, "1:1"),
        127: create_format("5120x2160p @100Hz", "64:27", 1485.0, "1:1"),
    }
)

# Reserved VIC codes (128-192)
reserved_formats = {
    vic: create_format("Reserved", "Reserved", 0.0, "Reserved")
    for vic in range(128, 193)
}
video_formats.update(reserved_formats)

# High VIC codes (193-219)
video_formats.update(
    {
        193: create_format("5120x2160p @120Hz", "64:27", 1485.0, "1:1"),
        194: create_format("7680x4320p @24Hz", "16:9", 1188.0, "1:1"),
        195: create_format("7680x4320p @25Hz", "16:9", 1188.0, "1:1"),
        196: create_format("7680x4320p @30Hz", "16:9", 1188.0, "1:1"),
        197: create_format("7680x4320p @48Hz", "16:9", 2376.0, "1:1"),
        198: create_format("7680x4320p @50Hz", "16:9", 2376.0, "1:1"),
        199: create_format("7680x4320p @60Hz", "16:9", 2376.0, "1:1"),
        200: create_format("7680x4320p @100Hz", "16:9", 4752.0, "1:1"),
        201: create_format("7680x4320p @120Hz", "16:9", 4752.0, "1:1"),
        202: create_format("7680x4320p @24Hz", "64:27", 1188.0, "4:3"),
        203: create_format("7680x4320p @25Hz", "64:27", 1188.0, "4:3"),
        204: create_format("7680x4320p @30Hz", "64:27", 1188.0, "4:3"),
        205: create_format("7680x4320p @48Hz", "64:27", 2376.0, "4:3"),
        206: create_format("7680x4320p @50Hz", "64:27", 2376.0, "4:3"),
        207: create_format("7680x4320p @60Hz", "64:27", 2376.0, "4:3"),
        208: create_format("7680x4320p @100Hz", "64:27", 4752.0, "4:3"),
        209: create_format("7680x4320p @120Hz", "64:27", 4752.0, "4:3"),
        210: create_format("10240x4320p @24Hz", "64:27", 1485.0, "1:1"),
        211: create_format("10240x4320p @25Hz", "64:27", 1485.0, "1:1"),
        212: create_format("10240x4320p @30Hz", "64:27", 1485.0, "1:1"),
        213: create_format("10240x4320p @48Hz", "64:27", 2970.0, "1:1"),
        214: create_format("10240x4320p @50Hz", "64:27", 2970.0, "1:1"),
        215: create_format("10240x4320p @60Hz", "64:27", 2970.0, "1:1"),
        216: create_format("10240x4320p @100Hz", "64:27", 5940.0, "1:1"),
        217: create_format("10240x4320p @120Hz", "64:27", 5940.0, "1:1"),
        218: create_format("4096x2160p @100Hz", "256:135", 1188.0, "1:1"),
        219: create_format("4096x2160p @120Hz", "256:135", 1188.0, "1:1"),
    }
)
