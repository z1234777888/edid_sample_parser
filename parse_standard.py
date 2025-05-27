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
        HeaderParams.MF_id = HeaderInfo._parse_manufacturer_id(edid_data[8:10])
        HeaderParams.product_code = HeaderInfo._parse_product_code(edid_data[10:12])
        HeaderParams.serial_number = HeaderInfo._parse_serial_number(edid_data[12:16])
        HeaderParams.MF_week = str(edid_data[16])
        HeaderParams.MF_year = str(edid_data[17] + 1990)
        HeaderParams.version = f"{edid_data[18]}.{edid_data[19]}"

        print(f"製造商ID\t{HeaderParams.MF_id}")
        print(f"產品代碼\t{HeaderParams.product_code}")
        print(f"序列號碼\t{HeaderParams.serial_number}")
        print(f"製造週數\t{HeaderParams.MF_week}")
        print(f"製造年份\t{HeaderParams.MF_year}")
        print(f"EDID版本\t{HeaderParams.version}")

        print(f"{'='*10}header parse completed{'='*10}")

    @staticmethod
    def _parse_manufacturer_id(data: bytes) -> str:
        """解析製造商ID的輔助方法"""
        first = chr(((data[0] & 0x7C) >> 2) + 64)
        second = chr(((data[0] & 0x03) << 3) + ((data[1] & 0xE0) >> 5) + 64)
        third = chr((data[1] & 0x1F) + 64)
        return f"{first}{second}{third}"

    @staticmethod
    def _parse_product_code(data: bytes) -> str:
        """解析產品代碼"""
        return f"{(data[1] << 8) + data[0]:04X}"

    @staticmethod
    def _parse_serial_number(data: bytes) -> str:
        """解析序列號"""
        return f"{sum(b << (i * 8) for i, b in enumerate(data))}"
