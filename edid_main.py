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
