from enum import IntEnum
from vic_data.vic_to_formats import video_formats
from parser.parse_standard import get_freq
from vic_data.clock_to_formats import clock_to_formats
from parser.parse_standard import DTDParams


class TagCode(IntEnum):
    RESERVED = 0
    AUDIO = 1  # Audio Data Block
    VIDEO = 2  # Video Data Block
    VSDB = 3  # Vendor-Specific Data Block
    SPEAKER = 4  # Speaker Allocation Data Block
    VESA_DTC = 5  # VESA Display Transfer Characteristic Data Block
    VIDEO_FORMAT = 6  # Video Format Data Block
    EXTENDED = 7  # Use Extended Tag


def separate_tag_code(block: bytes, offset: int) -> tuple[int, int]:
    """分離tag code 和length"""
    tag_code = (block[offset] >> 5) & 0x07  # 取出前三位
    length = block[offset] & 0x1F  # 取出後五位
    return tag_code, length


header_offset = 1


class ParseCTATagCode:
    """解析CTA Data Block的Tag Code，目前只解析video、speaker與audio"""

    @staticmethod
    def parse_manager(block: bytes) -> list[dict[str, str]]:
        info: dict[str, str] = {}
        result: list[dict[str, str]] = []
        dtd_addr = block[2]
        current_offset = 4
        # 解析tag code直到dtd
        while current_offset < dtd_addr:
            tag_code, length = separate_tag_code(block, current_offset)

            # print(
            #     f"Tag Code: {tag_code},current_offset: {current_offset}, Length: {length}"
            # )
            # 更新offset，跳過header位元
            current_offset = current_offset + header_offset

            match tag_code:
                case TagCode.AUDIO:
                    # print("音訊格式")
                    info = ParseAudioTag.parse_manager(block, current_offset, length)
                case TagCode.VIDEO:
                    # print("影像格式")
                    info = ParseVideoTag.parse_manager(block, current_offset, length)
                case TagCode.SPEAKER:
                    # print("聲道配置")
                    info = ParseSpeakerBlock.parse_manager(
                        block, current_offset, length
                    )
                case TagCode.EXTENDED:
                    # print("跳過擴展格式")
                    info = ParseExtendedTag.parse_manager(block, current_offset, length)
                case TagCode.VSDB:
                    info = ParseVSDBBlock.parse_manager(block, current_offset, length)
                case _:
                    pass
            result.append(info)
            current_offset += length  # 更新offset

        return result


class YCbCr420CapParams:
    resolution: list[str] = []


class ParseYCbCr420CapabilityMap:
    """YCbCr 4:2:0 Capability Map Data Block"""

    @staticmethod
    def parse_manager(block: bytes, offset: int, length: int) -> str:
        result = ""
        print()
        print(f"{'='*10} YCbCr 4:2:0 Capability Map parse started {'='*10}")
        current_offset = offset + header_offset
        end_offset = (
            current_offset + length - 1
        )  # 長度是L-1 Bytes ，詳情參考cta-861-i章節7.5.11
        ParseYCbCr420CapabilityMap._parse_video_formats(
            block, current_offset, end_offset, VideoParams.resolution
        )
        result = f"支援YCbCr420的解析度: {", ".join(YCbCr420CapParams.resolution)}"
        print(result)
        print(f"{'='*10} YCbCr 4:2:0 Capability Map parse ended {'='*10}")
        return result

    @staticmethod
    def _parse_video_formats(
        block: bytes, current_offset: int, end_offset: int, res: list[str]
    ):
        """
        解析多位元組的位元資料

        Args:
            block: 位元組資料
            current_offset: 開始位置
            end_offset: 結束位置
            res: 對應的解析結果列表
        """
        data_bytes = block[current_offset:end_offset]
        YCbCr420CapParams.resolution.clear()
        bit_index = 0
        for byte_data in data_bytes:
            for bit_position in range(8):
                if byte_data & (1 << bit_position):
                    if bit_index < len(res):
                        YCbCr420CapParams.resolution.append(res[bit_index])
                bit_index += 1


class ParseExtendedTag:
    """解析CTA Extended Tag Code"""

    @staticmethod
    def parse_manager(block: bytes, offset: int, length: int) -> dict[str, str]:
        """解析Extended Tag Code"""

        tag_code = block[offset]
        name = identify_extended_tag(tag_code)
        info = ""
        # print(f"Extended Tag Code: {name}")

        if name == "HDR Static Metadata Data Block":
            info = ParseColorimetryBlock.parse_manager(block, offset, length)
            return {name: info}
        elif name == "YCbCr 4:2:0 Capability Map Data Block":
            info = ParseYCbCr420CapabilityMap.parse_manager(block, offset, length)
            return {name: info}
        else:
            return {name: info}


class HDRParams:
    support: list[str] = []
    code = {
        0: "SDR",
        1: "HDR",
        2: "HDR10",
    }


class ParseColorimetryBlock:

    @staticmethod
    def parse_manager(block: bytes, offset: int, length: int) -> str:
        """HDR 支援度"""
        print()
        print(f"{'='*10} Colorimetry Data Block parse started {'='*10}")
        current_offset = offset + header_offset
        tf_byte = block[current_offset]
        HDRParams.support.clear()

        for bit_position in range(3):
            if tf_byte & (1 << bit_position):
                HDRParams.support.append(HDRParams.code[bit_position])
        result = f"HDR 支援度: {', '.join(HDRParams.support)}"
        print(result)
        print(f"{'='*10} Colorimetry Data Block parse completed {'='*10}")
        return result


def identify_extended_tag(tag_code: int) -> str:
    """
    識別CTA Extended Tag Code並返回對應的資料類型描述

    Args:
        tag_code: Extended tag code值(0-255)

    Returns:
        str: 資料類型描述字串
    """
    # 使用字典映射tag code到描述
    extended_tag_map = {
        0: "Video Capability Data Block",
        1: "Vendor-Specific Video Data Block",
        2: "VESA Display Device Data Block [135]",
        3: "Reserved for VESA Video Data Block",
        4: "Reserved for HDMI Video Data Block [140]",
        5: "Colorimetry Data Block",
        6: "HDR Static Metadata Data Block",
        7: "HDR Dynamic Metadata Data Block",
        8: "Native Video Resolution Data Block",
        13: "Video Format Preference Data Block",
        14: "YCbCr 4:2:0 Video Data Block",
        15: "YCbCr 4:2:0 Capability Map Data Block",
        16: "Reserved for CTA Miscellaneous Audio Fields (MAF)",
        17: "Vendor-Specific Audio Data Block",
        18: "HDMI Audio Data Block [140]",
        19: "Room Configuration Data Block",
        20: "Speaker Location Data Block",
        32: "InfoFrame Data Block (includes one or more Short InfoFrame Descriptors)",
        34: "DisplayID Type VII Video Timing Data Block",
        35: "DisplayID Type VIII Video Timing Data Block",
        42: "DisplayID Type X Video Timing Data Block",
        120: "HDMI Forum EDID Extension Override Data Block [140]",
        121: "HDMI Forum Sink Capability Data Block [140]",
        122: "HDMI Forum Source-Based Tone Mapping Data Block [140]",
    }

    # 特殊範圍的處理
    if 9 <= tag_code <= 12:
        return "Reserved for video-related blocks"
    elif 21 <= tag_code <= 31:
        return "Reserved for audio-related blocks"
    elif 36 <= tag_code <= 41:
        return "Reserved"
    elif 43 <= tag_code <= 119:
        return "Reserved"
    elif 123 <= tag_code <= 127:
        return "Reserved for HDMI"
    elif 128 <= tag_code <= 255:
        return "Reserved"

    # 從映射字典中查找,如果找不到則返回"Unknown"
    return extended_tag_map.get(tag_code, "Unknown")


class VSDBParams:
    HDMI_IEEE_ID = 0x000C03

    dc_bit = {
        0: "10",
        1: "12",
        2: "16",
    }


class ParseVSDBBlock:
    @staticmethod
    def parse_manager(block: bytes, offset: int, length: int) -> dict[str, str]:
        """解析VSDB區塊"""
        info: dict[str, str] = {}
        ieee_id = (
            f"{block[offset] | block[offset + 1] << 8 | block[offset + 2] << 16:06x}"
        )
        if ieee_id == f"{VSDBParams.HDMI_IEEE_ID :06x}":
            print()
            print(f"{'='*10} VSDB parse started {'='*10}")
            # 剩餘資料為廠商自定義內容
            vendor_data = block[offset + 3 : offset + length] if length > 3 else bytes()
            cec_pa, res_support, color_depths, ycbcr_444_support = (
                ParseVSDBBlock._parse_hdmi_vsdb(vendor_data)
            )
            if cec_pa != "":
                info["CEC_PA"] = cec_pa
                print(f"CEC PA {info["CEC_PA"]}")

            if res_support != []:
                info["res_support"] = f"{', '.join(res_support)}"
                print(f"支援解析度 {info["res_support"]}")

            if color_depths != []:
                info["color_depths"] = f"{', '.join(color_depths)} bits"
                print(f"位元深度 {info["color_depths"] }")

            if ycbcr_444_support:
                print("支援  YCbCr 4:4:4 & RGB 4:4:4")
                info["rgb_444_support"] = "支援  YCbCr 4:4:4 & RGB 4:4:4"
            else:
                print("支援  RGB 4:4:4")
                info["rgb_444_support"] = "支援  RGB 4:4:4"

            print(f"{'='*10} VSDB parse ended {'='*10}")
            return info
        # else:
        #     print(
        #         f"未知的IEEE ID: {VSDBParams.ieee_id}, 目前只支援HDMI IEEE ID: {VSDBParams.HDMI_IEEE_ID:06x}"
        #     )
        return info

    @staticmethod
    def _parse_hdmi_vsdb(vendor_data: bytes) -> tuple[str, list[str], list[str], bool]:
        """解析HDMI VSDB內容"""
        # 如果忘記怎麼解析，可以找hdmi1.3 spec 或是看以下網址
        # https://blog.csdn.net/cfl927096306/article/details/108017501
        cec_pa: str = ""
        res_support: list[str] = []
        color_depths: list[str] = []
        ycbcr_444_support: bool = False

        if len(vendor_data) >= 2:
            # Physical Address
            pa_high = vendor_data[0]
            pa_low = vendor_data[1]
            cec_pa = f"{pa_high >> 4}.{pa_high & 0x0F}.{pa_low >> 4}.{pa_low & 0x0F}"

        if len(vendor_data) >= 3:
            features = vendor_data[2]
            color_deepth_support = (features & 0x70) >> 4
            for bit_position in range(3):
                if color_deepth_support & (1 << bit_position):
                    color_depths.append("".join(f"{VSDBParams.dc_bit[bit_position]}"))
            if (features & 0x08) >> 3:
                ycbcr_444_support = True

        if len(vendor_data) >= 4:
            tmds_clock = vendor_data[3] * 5

            h, v = DTDParams.perferred_HActive, DTDParams.perferred_VActive
            freq = get_freq(h, v, tmds_clock, clock_to_formats)
            if freq != 0:
                res_support.append(f"{h}x{v} @{freq}Hz" + f" - {tmds_clock} MHz")

        return cec_pa, res_support, color_depths, ycbcr_444_support


class AudioParams:
    supported_frequencies: list[str] = [""]
    LPCM_bit_depths: list[str] = [""]
    bit_rate: str = ""
    audio_spec: str = ""
    wma_profile_code: str = ""
    audio_format: str = ""
    SAMPLING_FREQS = {
        6: "192",
        5: "176.4",
        4: "96",
        3: "88.2",
        2: "48",
        1: "44.1",
        0: "32",
    }
    BIT_DEPTHS = {2: "24", 1: "20", 0: "16"}
    FORMAT_CODE = {
        0: "Unknown",
        1: "L-PCM",
        2: "AC-3",
        3: "MPEG-1",
        4: "MP3",
        5: "MPEG2",
        6: "AAC LC",
        7: "DTS",
        8: "ATRAC",
        9: "DSD",
        10: "E-AC-3",
        11: "DTS-HD/DTS-UHD",
        12: "MAT (MLP)",
        13: "DST",
        14: "WMA Pro",
        15: "Extended Audio",
    }


class ParseAudioTag:

    @staticmethod
    def parse_manager(block: bytes, offset: int, length: int) -> dict[str, str]:
        """解析音訊格式的tag code"""
        result: str = ""
        print()
        print(f"{'='*10} audio data block parse started {'='*10}")
        current_offset = offset
        while current_offset < offset + length:

            descriptor_data = block[current_offset : current_offset + length]
            # 解析 Audio Format Code 和 Max Channels
            code = (descriptor_data[0] & 0x78) >> 3
            max_channels = (descriptor_data[0] & 0x07) + 1

            # 解析支援的取樣率
            ParseAudioTag._parse_sampling_frequencies(descriptor_data)

            AudioParams.audio_format = AudioParams.FORMAT_CODE[code]

            result += f"{AudioParams.audio_format:7} [{' '.join(map(str, AudioParams.supported_frequencies)) }]kHz, {max_channels} channels"
            # 解析位元深度
            if AudioParams.audio_format == "L-PCM":  # L-PCM
                ParseAudioTag._parse_lpcm_bit_depths(descriptor_data)
                result += f", [{' '.join(map(str,AudioParams.LPCM_bit_depths))}] bit"
            elif code >= 2 and code <= 8:
                AudioParams.bit_rate = f"{(descriptor_data[2] * 8)}kHz"
                result += f", {AudioParams.bit_rate}"
            elif code >= 9 and code <= 13:
                AudioParams.audio_spec = f"{descriptor_data[2] }"
                result += f", {AudioParams.audio_spec}"
            elif code == 14:
                if descriptor_data[2] & 0xF8:
                    AudioParams.wma_profile_code = f"profile error"
                else:
                    AudioParams.wma_profile_code = f"profile error"
                result += f", {AudioParams.wma_profile_code}"
            result += "\n"
            current_offset += 3
        print(result)
        print(f"{'='*10} audio data block parse ended {'='*10}")
        return {"descriptor": result}

    @staticmethod
    def _parse_sampling_frequencies(descriptor_data: bytes):
        """解析取樣頻率"""
        AudioParams.supported_frequencies.clear()
        for bit_position in range(7):
            if descriptor_data[1] & (1 << bit_position):
                AudioParams.supported_frequencies.append(
                    AudioParams.SAMPLING_FREQS[bit_position]
                )

    @staticmethod
    def _parse_lpcm_bit_depths(descriptor_data: bytes):
        """解析LPCM位元深度"""
        AudioParams.LPCM_bit_depths.clear()
        for bit_position in range(3):
            if descriptor_data[2] & (1 << bit_position):
                AudioParams.LPCM_bit_depths.append(AudioParams.BIT_DEPTHS[bit_position])


class VideoParams:
    info: dict[str, str] = {}
    resolution: list[str] = []


class ParseVideoTag:

    @staticmethod
    def parse_manager(block: bytes, offset: int, length: int) -> dict[str, str]:
        """解析影像格式的tag code"""
        result: list[str] = []
        print()
        print(f"{'='*10} video data block parse started {'='*10}")
        VideoParams.resolution.clear()
        current_offset = offset

        while current_offset < offset + length:
            vic_byte = block[current_offset]

            if vic_byte <= 64:
                # native = bool(vic_byte & 0x80)
                vic = vic_byte & 0x7F
            else:
                # native = False
                vic = vic_byte

            VideoParams.info = ParseVideoTag._get_video_format_info(vic)

            result.append(
                f"VIC {vic:3d}, {VideoParams.info["resolution"]:18} {VideoParams.info["display_aspect_ratio"]} - {VideoParams.info["pixel_clock"]} MHz"
            )
            VideoParams.resolution.append(f"{VideoParams.info["resolution"]}")

            current_offset += 1
        print("\n".join(result))

        print(f"{'='*10} video data block parse ended {'='*10}")
        return {"descriptor": "| ".join(result)}

    @staticmethod
    def _get_video_format_info(vic: int) -> dict[str, str]:
        """解析VIC對應的視訊格式詳細參數

        Args:
            vic: Video Identification Code (1-255)

        Returns:
            包含解析後視訊參數的字典
        """
        format = video_formats.get(vic, {})

        return format


class SpeakerAllocation:
    speaker_config1 = {
        0: "FL/FR",
        1: "LFE",
        2: "FC",
        3: "BL/BR",
        4: "BC",
        5: "FLC/FRC",
        6: "RLC/RRC",
        7: "FLW/FRW",
    }
    speaker_config2 = {
        0: "TFL/TFR",
        1: "TFC",
        2: "TBL/TBR",
        3: "TBC",
        4: "TPFL/TPFR",
    }


class ParseSpeakerBlock:

    @staticmethod
    def parse_manager(block: bytes, offset: int, length: int) -> dict[str, str]:
        """解析聲道配置的tag code"""
        info: str = ""
        print()
        print(f"{'='*10} speaker data block parse started {'='*10}")

        current_offset = offset
        speaker_data = block[current_offset : current_offset + length]
        for bit_position in range(8):
            if speaker_data[0] & (1 << bit_position):
                info += f" - {SpeakerAllocation.speaker_config1[bit_position]}"

        for bit_position in range(4):
            if speaker_data[1] & (1 << bit_position):
                info += f" - {SpeakerAllocation.speaker_config2[bit_position]}"
        print(f"Speaker Configuration: {info}")

        print(f"{'='*10} speaker data block parse ended {'='*10}")
        return {"descriptor": info}
