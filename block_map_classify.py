from typing import Dict
from parser.parse_standard import (
    HeaderInfo,
    BasicDisplayParameters,
    DTDInfo,
    TimingInfo,
)
from parser.parse_cta_extension import ParseCTATagCode
from parser.parse_displayid import ParseDPBlock
from datatypes import (
    HeaderInfoData,
    TimingInfoData,
    StandardBlockResult,
    DTDInfoData,
    CTABlockResult,
    DisplayIDBlockResult,
)


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


class ParseStandardBlock:
    def parse(self, block: bytes) -> StandardBlockResult:
        return self._parse_standard_block(block)

    def _parse_standard_block(self, block: bytes) -> StandardBlockResult:
        """解析標準區塊"""
        result: StandardBlockResult = {}
        # 標頭解析
        header_info: HeaderInfoData = HeaderInfo.parse_manager(block)
        # Basic Display Parameters 解析
        BasicDisplayParameters.parse_manager(block)

        timing_info: TimingInfoData = TimingInfo.parse_manager(block)
        result["TimingInfo"] = timing_info
        # DTD 解析，只有CTA擴展區才需要額外宣告offset
        DTD_info: DTDInfoData = DTDInfo.parse_manager(block)
        # 組合結果
        result = {
            "HeaderInfo": header_info,
            "DTDInfo": DTD_info,
        }

        return result


class ParseCTABlock:
    def parse(self, block: bytes) -> CTABlockResult:
        return self._parse_cta_extension_block(block)

    def _parse_cta_extension_block(self, block: bytes) -> CTABlockResult:
        """解析CTA擴展區塊"""
        # 先解析tag code
        # block = test_block
        dtd_addr = block[2]
        tag_code_info = ParseCTATagCode.parse_manager(block)
        # DTD 解析，只有CTA擴展區才需要額外宣告offset
        DTD_info: DTDInfoData = DTDInfo.parse_manager(block, start_addr=dtd_addr)

        result: CTABlockResult = {"TagCodeInfo": tag_code_info, "DTDInfo": DTD_info}
        return result


class ParseDisplayIDBlock:
    def parse(self, block: bytes) -> DisplayIDBlockResult:
        return self._parse_display_id_block(block)

    def _parse_display_id_block(self, block: bytes) -> DisplayIDBlockResult:

        return {"Type_I": ParseDPBlock.parse_manager(block)}
