class StandardValidator:

    def header(self, block: bytes) -> bool:
        expected = bytes([0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00])

        if block[:8] == expected:
            print("標準區塊header:正確")
            return True
        else:
            print("標準區塊header:錯誤")
            print("should be", expected)
            print("but got", block[:8])
            return False


class CheckSumValidator:
    def extension_num(self, edid_data: bytes) -> bool:
        """只能使用在標準區塊，因為只有標準區有擴展數宣告"""
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

    def check_sum(self, block: bytes) -> bool:

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
