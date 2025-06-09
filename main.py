from monitor_info import MonitorManager
from block_map_classify import BlockMapBlock, ParseEdidBlock
from parse_standard import ENGINEERING
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


def extension_num(edid_data: bytes) -> bool:
    """檢查擴展數是否正確，須放置全部的edid，而非單一block"""
    # 計算總共有幾個完整的區塊
    total_blocks = len(edid_data) // 128

    # 取得擴充數量資料
    expected_extensions = edid_data[126]
    actual_extensions = total_blocks - 1
    # 儲存結果
    if actual_extensions == expected_extensions:
        print("擴展數正確")
        return True
    else:
        print("擴展數錯誤")
        print("should be", expected_extensions)
        print("but got", actual_extensions)
        return False


def check_sum(block: bytes) -> bool:

    # 取得預期的checksum (最後一個位元組)，並格式化為兩位十六進制
    expected_checksum = f"{block[-1]:02X}"

    # 計算前127個位元組的總和
    byte_sum = sum(block[:-1]) & 0xFF

    # 計算checksum (0 減去總和的結果)，並格式化為兩位十六進制
    actual_checksum = f"{(0 - byte_sum) & 0xFF:02X}"

    # 比較預期的checksum 和實際的checksum
    if expected_checksum == actual_checksum:
        print("checksum 正確")
        return True
    else:
        print("checksum 錯誤")
        print("should be", expected_checksum)
        print("but got", actual_checksum)
        return False


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

    print(f"偵測到 {len(info.active_monitors)} 個活躍顯示器")

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
            elif key == BlockType.BLOCK_MAP:
                pass
        if standard_block is not None:
            parse_edid.parse(standard_block)
            if ENGINEERING:
                check_sum(standard_block)

        if cta_extension_block is not None:
            parse_edid.parse(cta_extension_block)
            if ENGINEERING:
                check_sum(cta_extension_block)

        if display_id_block is not None:
            parse_edid.parse(display_id_block)
            if ENGINEERING:
                check_sum(display_id_block)

        # 比對擴展數
        if ENGINEERING:
            extension_num(raw_data)

        """每次結束解析時,將raw_data拋出來"""
        print()
        print(format_bytes(raw_data))

    print("\n程式執行完畢，如果有遺漏的顯示器，請將顯示設定改為延伸模式後再試一次")


if __name__ == "__main__":
    main()
