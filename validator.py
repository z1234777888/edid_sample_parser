from typing import Callable


class ValidationParams:
    year = 2025  # 隨著年份調整
    week = 54  # 不能超過53，一年只有53周
    block_length = 128  # 每個block只能128 Bytes
    header = bytes([0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00])  # 標準header
    version = 1.4  # 不能超過1.4


class StandardValidator:
    @staticmethod
    def validate_manager(data: bytes):
        """驗證基礎項目"""
        print()
        print(f"{'='*10}validation started{'='*10}")
        # 所有驗證函數和參數
        checks: list[tuple[str, Callable[[bytes], None], bytes]] = [
            ("type", StandardValidator._validate_type, data),
            ("header", StandardValidator._validate_header, data),
            ("length", StandardValidator._validate_length, data),
            ("week", StandardValidator._validate_week, data),
            ("year", StandardValidator._validate_year, data),
            ("version", StandardValidator._validate_version, data),
        ]

        for index, (name, func, args) in enumerate(checks):

            try:
                func(args)
                print(f"{index+1}. ✓ {name} 驗證通過")
            except (TypeError, ValueError) as e:
                print(f"{index+1}. ✗ {name} 驗證失敗: {e}")

        print(f"{'='*10}validation completed{'='*10}")

    @staticmethod
    def _validate_type(data: bytes):

        s = f"file type is {type(data)}"
        if not isinstance(data, bytes):
            raise TypeError(f"{s}......error, data must be bytes")
        # else:
        #     print(f"{s}......ok")

    @staticmethod
    def _validate_length(data: bytes):

        s = f"length is {len(data)}"
        if len(data) < ValidationParams.block_length:
            raise ValueError(f"{s}......error, block must be 128 bytes")
        # else:
        #     print(f"{s}......ok")

    @staticmethod
    def _validate_header(data: bytes):
        s = f"header is {data[0:8].hex()}"
        if data[0:8] != ValidationParams.header:
            raise ValueError(f"{s}......error, must be 00ffffffffffff00")
        # else:
        #     print(f"{s}......ok")

    @staticmethod
    def _validate_week(data: bytes):
        """驗證製造週數，可以是0-53"""
        # 小端序
        week = data[16]
        s = f"week is {week}"
        if week > ValidationParams.week:
            raise ValueError(f"{s}......error, must be less than 54")
        # else:
        #     print(f"{s}......ok")

    @staticmethod
    def _validate_year(data: bytes):
        """驗證製造年份"""
        # 小端序
        year = data[17] + 1990
        s = f"year is {year}"
        if year > ValidationParams.year:
            raise ValueError(f"{s}......error, must be less than 2025")
        # else:
        #     print(f"{s}......ok")

    @staticmethod
    def _validate_version(data: bytes):
        version_bytes = data[18:20]
        version_high = version_bytes[0]
        version_low = version_bytes[1]
        version = version_high + version_low / 10

        s = f"version is {version}"
        if version > ValidationParams.version:
            raise ValueError(f"{s}......error, must be less than 1.4")
        # else:
        #     print(f"{s}......ok")
