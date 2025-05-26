from typing import Dict
from validator import StandardValidator


class BlockMapBlock:
    def __init__(self):
        self.BLOCK_SIZE = 128
        self.MAP_TAG = 0xF0
        self.CTA_TAG = 0x02
        self.DISPLAY_TAG = 0x70
        self.STANDARD_TAG = 0x00

    def classify_blocks(self, edid_data: bytes) -> Dict[int, bytes]:
        sort_blocks: dict[int, bytes] = {}  # key為標籤值，value為bytes

        for i in range(0, len(edid_data), self.BLOCK_SIZE):

            block = edid_data[i : i + self.BLOCK_SIZE]
            tag = block[0]
            if tag == self.STANDARD_TAG:
                sort_blocks[0] = block
                # print("找到標準區塊")
            if tag == self.CTA_TAG:
                sort_blocks[1] = block
                # print("找到 CTA 擴展區塊")
            if tag == self.DISPLAY_TAG:
                sort_blocks[2] = block
                # print("找到display ID 區塊")
            if tag == self.MAP_TAG:
                sort_blocks[3] = block
                # print("找到block map區塊")

        return sort_blocks


class ParseEdidBlock(BlockMapBlock):
    def parse(self, block: bytes) -> Dict[str, str]:
        tag = block[0]

        match tag:
            case self.STANDARD_TAG:
                return self._parse_standard_block(block)
            case self.CTA_TAG:
                return self._parse_cta_extension_block(block)
            case self.DISPLAY_TAG:
                return self._parse_display_id_block(block)
            case self.MAP_TAG:
                return {}
            case _:
                return {}

    def _parse_standard_block(self, block: bytes) -> Dict[str, str]:
        validator = StandardValidator()
        validator.header(block)

        return {}

    def _parse_cta_extension_block(self, block: bytes) -> Dict[str, str]:
        return {}

    def _parse_display_id_block(self, block: bytes) -> Dict[str, str]:
        return {}
