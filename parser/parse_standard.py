from enum import IntEnum
from vic_data.clock_to_formats import clock_to_formats
from datatypes import (
    HeaderInfoData,
    TimingInfoData,
    StaTimingItem,
    EstTimingItem,
    DTDInfoData,
)
from typing import Tuple


class HeaderParams:
    MF_id = "KEN"  # manufacturer id
    product_code = "1234"
    serial_number = "321321"
    MF_week = "WW"  # manufactured date
    MF_year = "YY"  # manufactured year
    version = "1.4"


class HeaderInfo:
    """解析標頭資訊"""

    @staticmethod
    def parse_manager(edid_data: bytes) -> HeaderInfoData:
        """組合標頭數據"""
        result: HeaderInfoData = {}
        print()
        print(f"{'='*10}header parse started{'='*10}")
        HeaderParams.MF_id = HeaderInfo._parse_manufacturer_id(edid_data)
        HeaderParams.product_code = HeaderInfo._parse_product_code(edid_data)
        HeaderParams.serial_number = HeaderInfo._parse_serial_number(edid_data)
        HeaderParams.MF_week = HeaderInfo._parse_week(edid_data)
        HeaderParams.MF_year = HeaderInfo._parse_year(edid_data)
        HeaderParams.version = HeaderInfo._parse_version(edid_data)

        print(f"製造商ID\t{HeaderParams.MF_id}")
        print(f"產品代碼\t{HeaderParams.product_code}")
        result["serial_number"] = HeaderParams.serial_number
        result["MF_week"] = HeaderParams.MF_week
        result["MF_year"] = HeaderParams.MF_year
        print(f"序列號碼\t{HeaderParams.serial_number}")
        print(f"製造週數\t{HeaderParams.MF_week}")
        print(f"製造年份\t{HeaderParams.MF_year}")
        print(f"EDID版本\t{HeaderParams.version}")
        result = {
            "MF_id": HeaderParams.MF_id,
            "product_code": HeaderParams.product_code,
            "version": HeaderParams.version,
        }
        print(f"{'='*10}header parse completed{'='*10}")
        return result

    @staticmethod
    def _parse_manufacturer_id(edid_data: bytes) -> str:
        """解析製造商ID的輔助方法"""
        data = edid_data[8:10]
        first = chr(((data[0] & 0x7C) >> 2) + 64)
        second = chr(((data[0] & 0x03) << 3) + ((data[1] & 0xE0) >> 5) + 64)
        third = chr((data[1] & 0x1F) + 64)
        return f"{first}{second}{third}"

    @staticmethod
    def _parse_product_code(edid_data: bytes) -> str:
        """解析產品代碼"""
        data = edid_data[10:12]
        return f"{(data[1] << 8) + data[0]:04X}"

    @staticmethod
    def _parse_serial_number(edid_data: bytes) -> str:
        """解析序列號"""
        data = edid_data[12:16]
        return f"{sum(b << (i * 8) for i, b in enumerate(data))}"

    @staticmethod
    def _parse_week(edid_data: bytes) -> str:
        """解析製造週數"""
        data = edid_data[16]
        return str(data)

    @staticmethod
    def _parse_year(edid_data: bytes) -> str:
        """解析製造年份"""
        data = edid_data[17]
        return str(data + 1990)

    @staticmethod
    def _parse_version(edid_data: bytes) -> str:
        """解析EDID版本"""
        data = edid_data[18:20]
        return f"{data[0]}.{data[1]}"


class EstablishedTimingInfo:

    @staticmethod
    def _get_timing1(timing_index: int) -> EstTimingItem:
        timing_configs = {
            0: {"resolution": "800x600", "refresh_rate": "60", "source": "VESA"},
            1: {"resolution": "800x600", "refresh_rate": "56", "source": "VESA"},
            2: {"resolution": "640x480", "refresh_rate": "75", "source": "VESA"},
            3: {"resolution": "640x480", "refresh_rate": "72", "source": "VESA"},
            4: {
                "resolution": "640x480",
                "refresh_rate": "67",
                "source": "Apple, Mac II",
            },
            5: {"resolution": "640x480", "refresh_rate": "60", "source": "IBM, VGA"},
            6: {"resolution": "720x400", "refresh_rate": "88", "source": "IBM, XGA2"},
            7: {"resolution": "720x400", "refresh_rate": "70", "source": "IBM, VGA"},
        }
        info = timing_configs.get(
            timing_index,
            {
                "resolution": "Undefined",
                "refresh_rate": "Undefined",
                "source": "Undefined",
            },
        )
        result: EstTimingItem = {
            "resolution": info["resolution"],
            "refresh_rate": info["refresh_rate"],
            "source": info["source"],
        }
        return result

    @staticmethod
    def _get_timing2(timing_index: int) -> EstTimingItem:
        timing_configs = {
            0: {
                "resolution": "1280x1024",
                "refresh_rate": "75",
                "source": "VESA",
            },
            1: {
                "resolution": "1024x768",
                "refresh_rate": "75",
                "source": "VESA",
            },
            2: {
                "resolution": "1024x768",
                "refresh_rate": "70",
                "source": "VESA",
            },
            3: {
                "resolution": "1024x768",
                "refresh_rate": "60",
                "source": "VESA",
            },
            4: {
                "resolution": "1024x768",
                "refresh_rate": "87",
                "source": "IBM",
                "note": "Interlaced",
            },
            5: {
                "resolution": "832x624",
                "refresh_rate": "75",
                "source": "Apple, Mac II",
            },
            6: {
                "resolution": "800x600",
                "refresh_rate": "75",
                "source": "VESA",
            },
            7: {
                "resolution": "800x600",
                "refresh_rate": "72",
                "source": "VESA",
            },
        }
        info = timing_configs.get(
            timing_index,
            {
                "resolution": "Undefined",
                "refresh_rate": "Undefined",
                "source": "Undefined",
            },
        )
        result: EstTimingItem = {
            "resolution": info["resolution"],
            "refresh_rate": info["refresh_rate"],
            "source": info["source"],
        }
        return result

    @staticmethod
    def timing1(block: bytes) -> list[EstTimingItem]:
        result: list[EstTimingItem] = []
        timing_byte = block[35]
        if timing_byte:
            print("第一組標準時序:")
            for i in range(8):
                if timing_byte & (1 << i):
                    info = EstablishedTimingInfo._get_timing1(i)
                    result.append(info)
                    print(
                        f"{info["resolution"]} @ {info["refresh_rate"]}Hz ({info["source"]})"
                    )
        if not result:
            undefined_timing: EstTimingItem = {
                "resolution": "Undefined",
                "refresh_rate": "Undefined",
                "source": "Undefined",
            }
            result.append(undefined_timing)
        return result

    @staticmethod
    def timing2(block: bytes) -> list[EstTimingItem]:
        result: list[EstTimingItem] = []

        timing_byte = block[36]
        if timing_byte:
            print("第二組標準時序:")
            for i in range(8):
                if timing_byte & (1 << i):
                    info = EstablishedTimingInfo._get_timing2(i)
                    result.append(info)
                    print(
                        f"{info["resolution"]} @ {info["refresh_rate"]}Hz ({info["source"]})"
                    )
        if not result:
            undefined_timing: EstTimingItem = {
                "resolution": "Undefined",
                "refresh_rate": "Undefined",
                "source": "Undefined",
            }
            result.append(undefined_timing)
        return result


class TimingInfo:

    @staticmethod
    def parse_manager(block: bytes) -> TimingInfoData:
        StandardTiming = StandardTimingInfo()  # 因為用了實例化所以要先宣告
        result: TimingInfoData = {
            "Standard": [],
            "Established_1": [],
            "Established_2": [],
        }
        """組合標準時序資訊"""
        print()
        print(f"{'='*10}established timing parse started{'='*10}")

        result["Established_1"] = EstablishedTimingInfo.timing1(block)
        result["Established_2"] = EstablishedTimingInfo.timing2(block)

        print(f"{'='*10}established timing parse completed{'='*10}")

        print()
        print(f"{'='*10}standard timing parse started{'='*10}")
        result["Standard"] = StandardTiming.parse_manager(block)
        print(f"{'='*10}standard timing parse completed{'='*10}")

        return result


class StandardTimingInfo:
    """用於解析 EDID 中的 Standard Timing 資訊 (Byte 38-53)

    每組 Standard Timing 使用 2 bytes 來描述一個顯示模式：
    - 第一個 byte: 水平解析度 (計算方式為: (value + 31) * 8)
    - 第二個 byte:
        - bit 7-6: 寬高比 (16:10, 4:3, 5:4, 16:9)
        - bit 5-0: 更新率 (計算方式為: value + 60)
    """

    def __init__(self):
        # 定義常數
        self._START_BYTE = 38  # Standard Timing 開始位置
        self._BYTES_PER_TIMING = 2  # 每組 Timing 使用的 bytes 數

        # 定義寬高比對照表
        self._ASPECT_RATIOS = {
            0b00: "16:10",
            0b01: "4:3",
            0b10: "5:4",
            0b11: "16:9",
        }

    def parse_manager(self, block: bytes) -> list[StaTimingItem]:
        result: list[StaTimingItem] = []
        for i in range(8):
            start_index = self._START_BYTE + (i * self._BYTES_PER_TIMING)
            info = self._parse_single_timing(block[start_index], block[start_index + 1])
            result.append(info)
            if info["h_res"] == "Undefined":
                continue
            print(
                f"{info['h_res']}x{info['v_res']} @ {info['refresh_rate']}Hz ({info['aspect_ratio']})"
            )
        if not result:
            unknown_timing: StaTimingItem = {
                "h_res": "Undefined",
                "v_res": "Undefined",
                "refresh_rate": "Undefined",
                "aspect_ratio": "Undefined",
            }
            result.append(unknown_timing)
        return result

    def _calculate_horizontal_resolution(self, value: int) -> int:
        """計算水平解析度"""
        if value == 0x01:  # 未使用的欄位
            return 0
        return (value + 31) * 8

    def _calculate_vertical_resolution(self, h_res: int, aspect_ratio: str) -> int:
        """根據水平解析度和寬高比計算垂直解析度"""
        if h_res == 0:
            return 0

        width, height = map(int, aspect_ratio.split(":"))
        return int(h_res * height / width)

    def _parse_single_timing(self, byte1: int, byte2: int) -> StaTimingItem:
        """解析單組 Standard Timing"""
        # 檢查是否為未使用的欄位
        if byte1 == 0x01 and byte2 == 0x01:
            return {
                "h_res": "Undefined",
                "v_res": "Undefined",
                "refresh_rate": "Undefined",
                "aspect_ratio": "Undefined",
            }

        # 解析水平解析度
        h_res = self._calculate_horizontal_resolution(byte1)

        # 解析寬高比
        aspect_ratio_bits = (byte2 >> 6) & 0b11
        aspect_ratio = self._ASPECT_RATIOS[aspect_ratio_bits]

        # 計算垂直解析度
        v_res = self._calculate_vertical_resolution(h_res, aspect_ratio)

        # 解析更新率
        refresh_rate = (byte2 & 0b111111) + 60
        h_res = f"{h_res}"
        v_res = f"{v_res}"
        refresh_rate = f"{refresh_rate}"
        return {
            "h_res": h_res,
            "v_res": v_res,
            "refresh_rate": refresh_rate,
            "aspect_ratio": aspect_ratio,
        }


class DTDParams:
    """DTD或display descriptor參數"""

    FIRST_DESCRIPTOR_ADDR = 0x36  # perferred timing 的位址
    DESCRIPTOR_SIZE = 18  # 每個DTD或display descriptor的大小
    EDID_BLOCK_SIZE = 128  # EDID的最大長度
    perferred_timing_info = "Undefined"
    perferred_HActive: int = 0
    perferred_VActive: int = 0
    timing_resolution = "Undefined"
    DESCRIPTOR_TAGS = {
        0xFF: "display_serial_number",
        0xFE: "ascii_string",
        0xFD: "display_range_limits",
        0xFC: "display_product_name",
        0xFB: "color_point_data",
        0xFA: "standard_timing",
        0xF9: "dcm_data",
        0xF8: "cvt_timing",
        0xF7: "established_timings_3",
        0x10: "dummy_descriptor",
    }


class DTDInfo:
    @staticmethod
    def parse_manager(
        block: bytes,
        start_addr: int = DTDParams.FIRST_DESCRIPTOR_ADDR,
        offset: int = DTDParams.DESCRIPTOR_SIZE,
    ) -> DTDInfoData:
        result: DTDInfoData = {}
        descriptor_info: dict[str, dict[str, str]] = {}
        timing_info: list[str] = []
        current_addr = start_addr  # 當前的DTD位址
        dtd_len = (
            DTDParams.EDID_BLOCK_SIZE - current_addr
        ) // DTDParams.DESCRIPTOR_SIZE
        print()
        # for i in range(dtd_len):
        #     print(
        #         " ".join(
        #             f"{byte:02x}"
        #             for byte in block[
        #                 current_addr
        #                 + i * DTDParams.DESCRIPTOR_SIZE : current_addr
        #                 + (i + 1) * DTDParams.DESCRIPTOR_SIZE
        #             ]
        #         )
        #     )
        print(f"{'='*10}DTD or Display Descriptor parse started{'='*10}")
        # 在base EDID處理perferred timing的解析
        if block[:8] == bytes([0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]):
            DTDInfo.parse_perfered_timing(block)
            current_addr += DTDParams.DESCRIPTOR_SIZE  # 取得下一個DTD的位址
            perferred_timing = DTDParams.perferred_timing_info
            print(f"首選時序解析度: {perferred_timing}")
            result["perferred_timing"] = perferred_timing
            dtd_len = 3

        # 最多3組
        for _ in range(dtd_len):
            # 如果下一組DTD的位址超過EDID的最大長度，就跳出迴圈
            if offset + DTDParams.DESCRIPTOR_SIZE > DTDParams.EDID_BLOCK_SIZE:
                break
            is_display_descriptor = (
                block[current_addr] == 0 and block[current_addr + 1] == 0
            )

            if is_display_descriptor:
                type, descriptor = DTDInfo.parse_display_descriptor(block, current_addr)
                descriptor_info[type] = descriptor
            else:
                DTDInfo.parse_timing_resolution(block, current_addr)
                timing_resolution = DTDParams.timing_resolution
                print(f"時序解析度: {timing_resolution}")
                timing_info.append(timing_resolution)

            current_addr += DTDParams.DESCRIPTOR_SIZE  # 取得下一個DTD的位址
        result["dtd_timing"] = timing_info
        result["dp_descriptor"] = descriptor_info
        print(f"{'='*10}DTD or Display Descriptor parse completed{'='*10}")

        return result

    @staticmethod
    def parse_display_descriptor(
        block: bytes, offset: int
    ) -> Tuple[str, dict[str, str]]:
        result: dict[str, str] = {}
        tag = block[offset + 3]
        descriptor_type = DTDParams.DESCRIPTOR_TAGS.get(tag, "reserved")
        # print(f"型態代碼{descriptor_type}")
        decriptor_data = block[offset + 5 : offset + DTDParams.DESCRIPTOR_SIZE]
        max_pixel_clock = block[offset + 9] * 10  # MHz
        h_active, v_active = DTDInfo.parse_perfered_timing(block)
        freq = get_freq(
            h_active, v_active, max_pixel_clock, clock_to_formats
        )  # 計算頻率

        if descriptor_type == "display_range_limits":
            range_limits = f"{h_active}x{v_active} @{freq}Hz {max_pixel_clock}MHz"
            max_rate = f"{block[offset + 6]} Hz"
            print("最大時序解析度: " + range_limits)
            print("最大垂直更新率: " + max_rate)
            result["max_resolution"] = range_limits
            result["max_refresh_rate"] = max_rate

        if descriptor_type == "display_serial_number":
            serial_number: str = f"{decriptor_data.decode("utf-8").strip()}"
            print("序列號碼: " + serial_number)
            result["SerialNumber"] = serial_number

        if descriptor_type == "ascii_string":
            ascii_string: str = f"{decriptor_data.decode('utf-8').strip()}"
            print("文字敘述: " + ascii_string)
            result["AsciiString"] = ascii_string

        if descriptor_type == "display_product_name":
            product_name: str = f"{decriptor_data.decode('utf-8').strip()}"
            print("產品名稱: " + product_name)
            result["ProductName"] = product_name

        return descriptor_type, result

    @staticmethod
    def parse_perfered_timing(block: bytes) -> tuple[int, int]:
        """解析首選的時序，僅在base edid 的[0x36]開始的第一組18位元組成"""
        h, v = DTDInfo.parse_timing_resolution(block)
        return h, v

    @staticmethod
    def parse_timing_resolution(
        block: bytes, offset: int = DTDParams.FIRST_DESCRIPTOR_ADDR
    ) -> tuple[int, int]:
        """解析時序解析度，暫時只解析必要的內容"""
        if block[offset + 17] == 0:
            print("dtd offset error")

        _clock = block[offset + 1] << 8 | block[offset]
        pixel_clock = _clock / 100.0  # MHz
        # 水平參數
        h_active = ((block[offset + 4] & 0xF0) << 4) | block[offset + 2]
        h_blanking = ((block[offset + 4] & 0x0F) << 8) | block[offset + 3]

        # 垂直參數
        v_active = ((block[offset + 7] & 0xF0) << 4) | block[offset + 5]
        v_blanking = ((block[offset + 7] & 0x0F) << 8) | block[offset + 6]

        h_total = h_active + h_blanking
        v_total = v_active + v_blanking
        if h_total == 0:
            h_total = 1
        if v_total == 0:
            v_total = 1
        refresh_rate = pixel_clock * 1000000 / (h_total * v_total)
        freq = int(round(refresh_rate, 0))

        if offset == DTDParams.FIRST_DESCRIPTOR_ADDR:
            DTDParams.perferred_timing_info = (
                f"{h_active}x{v_active} @{freq}Hz - {pixel_clock}MHz"
            )
            DTDParams.perferred_HActive = h_active
            DTDParams.perferred_VActive = v_active
        else:
            DTDParams.timing_resolution = (
                f"{h_active}x{v_active} @{freq}Hz - {pixel_clock}MHz"
            )
        return h_active, v_active


def get_freq(
    h_active: int,
    v_active: int,
    pixel_clock: float,
    clock_to_formats: list[tuple[int, int, int, float]],
) -> int:

    matching_freqs = [
        (freq, fourth_param)
        for h, v, freq, fourth_param in clock_to_formats
        if h == h_active and v == v_active and fourth_param <= pixel_clock
    ]

    if not matching_freqs:
        matching_freqs = [
            (freq, fourth_param)
            for h, v, freq, fourth_param in clock_to_formats
            if h == h_active and v <= v_active and fourth_param <= pixel_clock
        ]

    if not matching_freqs:
        return 0

    # 找出最大的 (fourth_param, freq) 組合
    return max(matching_freqs, key=lambda x: (x[1], x[0]))[0]


class BasicDisplayParameters:
    """解析Byte 20-24的參數"""

    @staticmethod
    def parse_manager(edid_data: bytes):
        """組合基本顯示器參數"""
        print()
        print(f"{'='*10}basic display parameters parse started{'='*10}")

        print(f"顯示器輸入類型")
        MonitorInputType.parse_manager(edid_data)

        print(f"{'='*10}basic display parameters parse completed{'='*10}")


class InputTypeParams:
    input_type = "Digital"
    # Digital
    color_depth = "Undefined"
    interface = "Undefined"
    # Analog
    signal_level_standard = "+0.7/−0.3 V"
    separate_sync = "Separate Sync H & V Signals are not supported"
    composite_sync = "Composite Sync Signal on Horizontal is not supported"
    composite_sync_green_video = "Composite Sync Signal on Green Video is not supported"
    serrations_v_sync = "Serration on the Vertical Sync is not supported"


class BitDepth(IntEnum):
    UNDEFINED = 0
    SIX_BITS = 1
    EIGHT_BITS = 2
    TEN_BITS = 3
    TWELVE_BITS = 4
    FOURTEEN_BITS = 5
    SIXTEEN_BITS = 6
    RESERVED = 7


class VideoInterface(IntEnum):
    UNDEFINED = 0
    DVI = 1
    HDMIa = 2
    HDMIb = 3
    MDDI = 4
    DisplayPort = 5


class SignalLevel(IntEnum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3


class MonitorInputType:
    """解析顯示器輸入類型"""

    @staticmethod
    def parse_manager(edid_data: bytes):
        """組合顯示器輸入類型"""

        # 判斷輸入類型，只會是Digital或Analog
        MonitorInputType._video_input_definition(edid_data)
        print(f"輸入類型\t{InputTypeParams.input_type}")

        if InputTypeParams.input_type == "Digital":
            ParseDigitalParams.parse_digital_params(edid_data)

            print(f"色彩位元\t{InputTypeParams.color_depth}")
            print(f"輸入介面\t{InputTypeParams.interface}")
        else:
            ParseAnalogParams.parse_analog_params(edid_data)

            print(f"訊號基準\t{InputTypeParams.signal_level_standard}")
            print(f"單獨同步\t{InputTypeParams.separate_sync}")
            print(f"複合同步\t{InputTypeParams.composite_sync}")
            print(f"複合綠像\t{InputTypeParams.composite_sync_green_video}")
            print(f"垂直同步\t{InputTypeParams.serrations_v_sync}")

    @staticmethod
    def _video_input_definition(edid_data: bytes):
        """判斷輸入類型 1=Digital 0=Analog"""
        video_input_type = (edid_data[20] & 0x80) >> 7
        InputTypeParams.input_type = "Digital" if video_input_type else "Analog"


class ParseDigitalParams:
    """解析數位輸入參數"""

    @staticmethod
    def parse_digital_params(edid_data: bytes):
        """解析數位輸入參數"""

        # 獲取顏色深度描述
        ParseDigitalParams._get_bit_depth(edid_data)
        # 獲取輸入介面描述
        ParseDigitalParams._get_video_interface(edid_data)

    @staticmethod
    def _get_bit_depth(edid_data: bytes):
        bit_depth_value = (edid_data[20] & 0x70) >> 4
        descriptions = {
            BitDepth.UNDEFINED: "Undefined",
            BitDepth.SIX_BITS: "6 bits per color",
            BitDepth.EIGHT_BITS: "8 bits per color",
            BitDepth.TEN_BITS: "10 bits per color",
            BitDepth.TWELVE_BITS: "12 bits per color",
            BitDepth.FOURTEEN_BITS: "14 bits per color",
            BitDepth.SIXTEEN_BITS: "16 bits per color",
            BitDepth.RESERVED: "Reserved",
        }
        bit_depth = BitDepth(bit_depth_value)  # Convert int to BitDepth enum
        InputTypeParams.color_depth = descriptions.get(bit_depth, "Undefined")

    @staticmethod
    def _get_video_interface(edid_data: bytes):
        video_interface_value = edid_data[20] & 0x0F
        descriptions = {
            VideoInterface.UNDEFINED: "Undefined",
            VideoInterface.DVI: "DVI",
            VideoInterface.HDMIa: "HDMIa",
            VideoInterface.HDMIb: "HDMIb",
            VideoInterface.MDDI: "MDDI",
            VideoInterface.DisplayPort: "DisplayPort",
        }
        interface = VideoInterface(
            video_interface_value
        )  # Convert int to VideoInterface enum
        InputTypeParams.interface = descriptions.get(interface, "Undefined")


class ParseAnalogParams:
    """解析類比輸入參數"""

    @staticmethod
    def parse_analog_params(edid_data: bytes):
        """解析類比輸入參數"""
        ParseAnalogParams._get_signal_level_standard(edid_data)
        ParseAnalogParams._get_video_step(edid_data)
        ParseAnalogParams._get_synchronization_types(edid_data)
        ParseAnalogParams._get_serrations(edid_data)

    @staticmethod
    def _get_signal_level_standard(edid_data: bytes):
        levels = (edid_data[20] & 0x60) >> 5

        descriptions = {
            SignalLevel.ZERO: "+0.7/−0.3 V",
            SignalLevel.ONE: "+0.714/−0.286 V",
            SignalLevel.TWO: "+1.0/−0.4 V",
            SignalLevel.THREE: "+0.7/0 V (EVC)",
        }
        levels = SignalLevel(levels)  # Convert int to WhiteSyncLevels enum
        InputTypeParams.signal_level_standard = descriptions.get(levels, "+0.7/−0.3 V")

    @staticmethod
    def _get_video_step(edid_data: bytes) -> str:
        step = (edid_data[20] & 0x10) >> 4
        return (
            "Blank-to-Black setup or pedestal" if step else "Blank Level = Black Level"
        )

    @staticmethod
    def _get_synchronization_types(edid_data: bytes):
        separate_sync = (edid_data[20] & 0x08) >> 3
        composite_sync = (edid_data[20] & 0x04) >> 2
        composite_sync_green_video = (edid_data[20] & 0x02) >> 1

        InputTypeParams.separate_sync = (
            "Separate Sync H & V Signals are supported"
            if separate_sync
            else "Separate Sync H & V Signals are not supported"
        )
        InputTypeParams.composite_sync = (
            "Composite Sync Signal on Horizontal is supported"
            if composite_sync
            else "Composite Sync Signal on Horizontal is not supported"
        )
        InputTypeParams.composite_sync_green_video = (
            "Composite Sync Signal on Green Video is supported"
            if composite_sync_green_video
            else "Composite Sync Signal on Green Video is not supported"
        )

    @staticmethod
    def _get_serrations(edid_data: bytes):
        serrations = edid_data[20] & 0x01
        InputTypeParams.serrations_v_sync = (
            "Serration on the Vertical Sync is supported"
            if serrations
            else "Serration on the Vertical Sync is not supported"
        )
