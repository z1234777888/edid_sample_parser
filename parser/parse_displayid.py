class TimingParams:
    # 確定timing區塊大小
    sizes = {
        0x03: 20,  # Type I
        0x04: 11,  # Type II
        0x05: 3,  # Type III
        0x06: 1,  # Type IV
        0x11: 7,  # Type V
        0x13: 17,  # Type VI
    }


class ParseDPBlock:

    @staticmethod
    def parse_manager(block: bytes) -> list[str]:
        result: list[str] = []
        version = block[1:2].hex()
        print(f"Version: {version}")
        print()
        print(f"{'='*10}display id parse started{'='*10}")
        current_offset = 5
        timing_tag = block[current_offset]
        timing_size = TimingParams.sizes.get(timing_tag)

        payload_length = block[current_offset + 2]

        if timing_size is not None:
            num_timings = payload_length // timing_size

            for i in range(num_timings):

                start = 8 + (i * timing_size)
                end = start + timing_size

                if end <= len(block):
                    timing_data = block[start:end]
                    match timing_tag:
                        case 0x03:
                            result.append(ParseDPBlock._parse_Type_I(timing_data))
                        case _:
                            tag_name = identify_displayid_block_type(timing_tag)
                            print(f"Display ID Timing Type not supported {tag_name}")

        print(f"{'='*10}display id parse completed{'='*10}")
        return result

    @staticmethod
    def _parse_Type_I(timing_data: bytes) -> str:
        # 解析像素時脈
        pixel_clock = timing_data[0] | timing_data[1] << 8 | timing_data[2] << 16
        pixel_clock = (
            pixel_clock / 100.0
        )  # 轉換為MHz，最小為0.01MHz，最大為167,772.16MHz

        # 解析timing首選
        Timing_Options = bool(timing_data[3] & 0x80)
        # Stereo_Support = (timing_data[3] & 0x60) >> 5
        # Interface_Frame_Scanning_Type = bool(timing_data[3] & 0x10)
        # Aspect_Ratio = timing_data[3] & 0x0F

        # 解析水平參數
        H_Active = (timing_data[4] | timing_data[5] << 8) + 1
        Horizontal_Blank_Pixels = (timing_data[6] | timing_data[7] << 8) + 1
        # Horizontal_Front_Porch = (timing_data[8] | (timing_data[9] & 0x7F) << 8) + 1
        Horizontal_Sync_Polarity = bool(timing_data[9] & 0x80)
        # Horizontal_Sync_Width = (timing_data[10] | timing_data[11] << 8) + 1

        if Horizontal_Sync_Polarity == True:
            Horizontal_Sync_Polarity = "Positive"
        else:
            Horizontal_Sync_Polarity = "Negative"

        # 解析垂直參數
        V_Active = (timing_data[12] | timing_data[13] << 8) + 1
        Vertical_Blank_Lines = (timing_data[14] | timing_data[15] << 8) + 1
        # Vertical_Front_Porch = (timing_data[16] | (timing_data[17] & 0x7F) << 8) + 1
        Vertical_Sync_Polarity = bool(timing_data[17] & 0x80)
        # Vertical_Sync_Width = (timing_data[18] | timing_data[19] << 8) + 1

        if Vertical_Sync_Polarity == True:
            Vertical_Sync_Polarity = "Positive"
        else:
            Vertical_Sync_Polarity = "Negative"

        # 計算總行數和總像素數
        h_total = H_Active + Horizontal_Blank_Pixels
        v_total = V_Active + Vertical_Blank_Lines

        # 計算更新率
        refresh_rate = pixel_clock * 1000000 / (h_total * v_total)
        result = f"{H_Active}x{V_Active} @{refresh_rate:.0f}Hz - {pixel_clock:.2f} MHz  {"(首選時序)" if Timing_Options else ""}"
        print("時序解析度: " + result)

        return result


def identify_displayid_block_type(timing_tag: int) -> str:
    """識別DisplayID數據塊類型"""
    types_map = {
        0x00: "Product Identification Data Block",
        0x01: "Display Parameters Data Block",
        0x02: "Color Characteristics Data Block",
        0x03: "Type I Timing - Detailed",
        0x04: "Type II Timing - Detailed",
        0x05: "Type III Timing - Short",
        0x06: "Type IV Timing - DMT ID Code",
        0x07: "VESA Timing Standard",
        0x08: "CEA Timing Standard",
        0x09: "Video Timing Range Limits",
        0x0A: "Product Serial Number",
        0x0B: "General Purpose ASCII String",
        0x0C: "Display Device Data Block",
        0x0D: "Interface Power Sequencing",
        0x0E: "Transfer Characteristics",
        0x0F: "Display Interface",
        0x10: "Stereo Display Interface",
        0x11: "Type V Timing - Short",
        0x12: "Tiled Display Topology",
        0x13: "Type VI Timing - Detailed",
    }
    return types_map.get(timing_tag, f"Unknown timing Type code(0x{timing_tag:02X})")
