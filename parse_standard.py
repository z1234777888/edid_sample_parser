from enum import IntEnum


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
    def parse_manager(edid_data: bytes):
        """組合標頭數據"""
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
        print(f"序列號碼\t{HeaderParams.serial_number}")
        print(f"製造週數\t{HeaderParams.MF_week}")
        print(f"製造年份\t{HeaderParams.MF_year}")
        print(f"EDID版本\t{HeaderParams.version}")

        print(f"{'='*10}header parse completed{'='*10}")

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


class MonitorSize:
    """顯示器尺寸資訊"""

    @staticmethod
    def parse_manager(edid_data: bytes):
        """組合顯示器尺寸資訊"""

        horizontal = edid_data[21]  # 位址15h
        vertical = edid_data[22]  # 位址16h

        if horizontal == 0 and vertical == 0:
            MonitorSize._parse_undefined_size()
        elif vertical == 0:
            MonitorSize._parse_landscape_ratio(horizontal)
        elif horizontal == 0:
            MonitorSize._parse_portrait_ratio(vertical)
        else:
            MonitorSize._parse_physical_size(horizontal, vertical)
