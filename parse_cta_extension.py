from enum import IntEnum


class TagCode(IntEnum):
    RESERVED = 0
    AUDIO = 1  # Audio Data Block
    VIDEO = 2  # Video Data Block
    VENDOR = 3  # Vendor-Specific Data Block
    SPEAKER = 4  # Speaker Allocation Data Block
    VESA_DTC = 5  # VESA Display Transfer Characteristic Data Block
    VIDEO_FORMAT = 6  # Video Format Data Block
    EXTENDED = 7  # Use Extended Tag


def separate_tag_code(block: bytes, offset: int) -> tuple[int, int]:
    """分離tag code 和length"""
    tag_code = (block[offset] >> 5) & 0x07  # 取出前三位
    length = block[offset] & 0x1F  # 取出後五位
    return tag_code, length


class ParseCTATagCode:
    """解析CTA Data Block的Tag Code，目前只解析video、speaker與audio"""

    @staticmethod
    def parse_manager(block: bytes):
        dtd_offset = block[2]
        current_offset = 4
        header_offset = 1
        # 解析tag code直到dtd
        while current_offset < dtd_offset:
            tag_code, length = separate_tag_code(block, current_offset)
            current_offset += length + header_offset
            match tag_code:
                case TagCode.AUDIO:
                    print("音訊格式")
                case TagCode.VIDEO:
                    print("影像格式")
                case TagCode.SPEAKER:
                    print("聲道配置")
                case _:
                    pass
