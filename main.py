from monitor_info import MonitorManager
from block_map_classify import BlockMapBlock, ParseEdidBlock
from validator import CheckSumValidator
from typing import List
from enum import IntEnum


def format_bytes(data: bytes):
    # 將 bytes 轉換為十六進位字串，每兩個字元一組
    hex_str = data.hex()
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


def main():

    manager = MonitorManager()
    info = manager.monitor_read()
    block_map = BlockMapBlock()
    parse_edid = ParseEdidBlock()
    raw_data = None  # bytes類型只能用optical，so that's why it's None by default
    standard_block = None
    cta_extension_block = None
    display_id_block = None
    if not info.active_monitors:
        print("未找到活耀顯示器資訊")
        return

    print(f"偵測到 {len(info.active_monitors)} 個活躍顯示器\n")

    for index, monitor in enumerate(info.active_monitors, 1):
        raw_data = manager.display_monitor_info(index, monitor, info.registry_paths)
        """這裡放置想要進一步解析的內容"""
        if raw_data is None:
            continue

        for key, value in block_map.classify_blocks(raw_data).items():
            if key == BlockType.STANDARD:
                standard_block = value

            elif key == BlockType.CTA_EXTENSION:
                cta_extension_block = value
            elif key == BlockType.DISPLAY_ID:
                display_id_block = value

        if standard_block is not None:
            parse_edid.parse(standard_block)
            CheckSumValidator.check_sum(standard_block)

        if cta_extension_block is not None:
            parse_edid.parse(cta_extension_block)
            CheckSumValidator.check_sum(cta_extension_block)

        if display_id_block is not None:
            parse_edid.parse(display_id_block)
            CheckSumValidator.check_sum(display_id_block)

        # 比對擴展數
        CheckSumValidator.extension_num(raw_data)

        """每次結束解析時,將raw_data拋出來"""
        print(format_bytes(raw_data))
        print()

    print("\n程式執行完畢")


if __name__ == "__main__":
    main()
