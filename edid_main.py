from monitor_info import MonitorManager
from block_map_classify import (
    BlockMapBlock,
    ParseStandardBlock,
    ParseCTABlock,
    ParseDisplayIDBlock,
)
from validator import StandardValidator
from typing import List
from enum import IntEnum

from datatypes import TotalResult


def format_bytes(data: bytes):
    # 將 bytes 轉換為十六進位字串，每兩個字元一組
    hex_str = data.hex().upper()
    pairs = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    # 每16組加換行符號
    lines: List[str] = []
    for i in range(0, len(pairs), 16):
        line = " ".join(pairs[i : i + 16])
        lines.append(line)

        # 每8行（128組）後加額外換行
        if (i // 16 + 1) % 8 == 0 and i + 16 < len(pairs):
            lines.append("")  # 空行

    return "\n".join(lines)


class BlockType(IntEnum):
    STANDARD = 0
    CTA_EXTENSION = 1
    DISPLAY_ID = 2
    BLOCK_MAP = 3


def EDID_parse_manager(raw_data: bytes) -> TotalResult:
    block_map = BlockMapBlock()
    sta = ParseStandardBlock()
    cta = ParseCTABlock()
    dpid = ParseDisplayIDBlock()
    result: TotalResult = {}

    check_sum_result: list[bool] = []
    for key, value in block_map.classify_blocks(raw_data).items():
        if key == BlockType.STANDARD:
            standard_block = value
            StandardValidator.validate_manager(standard_block)
            result["StandardBlockInfo"] = sta.parse(standard_block)

        elif key == BlockType.CTA_EXTENSION:
            cta_extension_block = value
            result["CTABlockInfo"] = cta.parse(cta_extension_block)
            result["check_dtd_offset"] = (
                "DTD 偏移位址正確"
                if result["CTABlockInfo"]["dtd_offset"] == int.from_bytes(value[2:3])
                else "DTD 偏移位址錯誤，應該為 "
                + f"{value[2:3].hex()}"
                + "實際為 "
                + f"{result['CTABlockInfo']['dtd_offset']:02x}"
            )
            print(
                "dtd_offset 正確" if result["check_dtd_offset"] else "dtd_offset 錯誤"
            )
        elif key == BlockType.DISPLAY_ID:
            display_id_block = value
            result["DisplayIDBlockInfo"] = dpid.parse(display_id_block)

        elif key == BlockType.BLOCK_MAP:
            pass
        check_sum_result.append(StandardValidator.check_sum(value))
    # 比對擴展數
    result["Checksum"] = [
        "Checksum 正確" if x else "Checksum 錯誤" for x in check_sum_result
    ]

    result["ExtensionNum"] = (
        "擴展數正確" if StandardValidator.extension_num(raw_data) else "擴展數錯誤"
    )
    return result


def main() -> list[TotalResult]:

    manager = MonitorManager()
    monotor_info = manager.monitor_read()

    EDID_info: TotalResult = {}
    EDID_info_list: list[TotalResult] = []

    if not monotor_info.active_monitors:
        print("未找到活耀顯示器資訊")
        return []

    print(f"偵測到 {len(monotor_info.active_monitors)} 個活躍顯示器")

    for index, monitor in enumerate(monotor_info.active_monitors, 1):
        raw_data = manager.display_monitor_info(
            index, monitor, monotor_info.registry_paths
        )
        """這裡放置想要進一步解析的內容"""
        if raw_data is None:
            continue

        # raw_data = "00 FF FF FF FF FF FF 00 09 D1 ED 7F FF FF FF FF FF FF 01 03 80 36 1E 78 2A CD 35 AF 4E 3E B2 27 0F 50 54 A5 6B 80 D1 C0 81 C0 81 00 81 80 A9 C0 B3 00 81 BC 01 01 02 3A 80 18 71 38 2D 40 58 2C 45 00 18 2A 21 00 00 1E 00 00 00 FF 00 30 30 30 30 30 30 30 30 30 30 53 4C 30 00 00 00 FD 0A 18 FF 1E F3 AB 00 0A 20 20 20 20 20 20 00 00 00 FC 00 58 4C 32 35 38 36 58 2B 0A 20 20 20 20 01 3B 02 03 4B F1 E2 78 02 4F 90 05 04 03 02 01 12 11 13 3F 07 06 1F 20 40 E2 00 CF 23 09 07 07 83 01 00 00 67 03 0C 00 30 00 00 44 6D D8 5D C4 01 78 80 40 02 00 00 81 44 15 72 1A 00 00 03 01 3C F0 E6 00 00 00 00 00 58 02 00 00 00 B4 91 00 A0 50 C0 78 30 30 20 35 00 18 2A 21 00 00 1A 0C DF 80 A0 70 38 40 40 30 40 35 00 18 2A 21 00 00 1A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 B0"
        # raw_data = raw_data.replace(" ", "")
        # raw_data = bytes.fromhex(raw_data)
        EDID_info = EDID_parse_manager(raw_data)
        EDID_info["EDIDRawData"] = format_bytes(raw_data)
        EDID_info_list.append(EDID_info)

        """每次結束解析時,將raw_data拋出來"""
        print()
        print(EDID_info["EDIDRawData"])

    print()

    print("\n程式執行完畢，如果有遺漏的顯示器，請將顯示設定改為延伸模式後再試一次")
    return EDID_info_list


if __name__ == "__main__":
    main()
