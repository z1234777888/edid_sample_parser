import sys

from branch_ico import get_branch_icon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)
from datetime import datetime

from PyQt6.QtWidgets import QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor

from edid_main import main as edid_parser
from datatypes import TotalResult
from typing import List, Dict, Match
import re

# 內嵌字體 Inconsolata SemiExpanded
from embedded_fonts import load_embedded_fonts


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_info_type_selection = "完整檢視"  # 保存下拉選單狀態或首次狀態
        self.is_dark_mode = False

        self.parsed_data_list: list[TotalResult] = []
        self.separator_lines = False
        self.themes = {
            "light": """
                QMainWindow {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QLabel {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QPushButton {
                    background-color: #F0F0F0;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    padding: 5px;
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
                QPushButton:focus {
                    border: 1px solid #CCCCCC;
                    outline: none;
                }
                QComboBox {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                }
                QTextEdit {
                    background-color: #F5F5F5;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    font-family: Inconsolata semiexpanded;
                }
            """,
            "dark": """
                QMainWindow {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                QLabel {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                QPushButton {
                    background-color: #3D3D3D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    padding: 5px;
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #4D4D4D;
                }
                QPushButton:focus {
                    border: 1px solid #555555;
                    outline: none;
                }
                QComboBox {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #3D3D3D;
                }
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #58c2e5;
                    border: 1px solid #3D3D3D;
                    font-family: Inconsolata semiexpanded;
                }
            """,
        }

        self.initUI()

    def initUI(self):
        self.setWindowTitle("EDID解析器")

        self.setWindowIcon(get_branch_icon())
        self.resize(840, 500)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create toolbar
        toolbar = QHBoxLayout()

        # Font size controls
        font_label = QLabel("字體大小:")
        self.decrease_btn = QPushButton("-")
        self.decrease_btn.setFixedWidth(30)
        self.font_size_label = QLabel("13")
        self.font_size_label.setFixedWidth(30)
        self.font_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.increase_btn = QPushButton("+")
        self.increase_btn.setFixedWidth(30)

        # 顯示器數量label
        self.monitor_count_label = QLabel("目前顯示器數量: 0")
        self.monitor_count_label.setStyleSheet("margin-left: 60px;")  # 加一些間距

        # Create text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setAcceptRichText(True)  # 允許富文本

        # INCONSOLATA_SEMIEXPANDED-REGULAR
        font_family = load_embedded_fonts()

        self.text_display.setFont(QFont(font_family, int(self.font_size_label.text())))
        # Other controls
        self.refresh_btn = QPushButton("重新整理顯示器資訊")
        self.export_btn = QPushButton("匯出資訊")

        self.theme_btn = QPushButton("切換夜間模式")

        self.labels = [font_label, self.font_size_label, self.monitor_count_label]

        # Add controls to toolbar
        toolbar.addWidget(font_label)
        toolbar.addWidget(self.decrease_btn)
        toolbar.addWidget(self.font_size_label)
        toolbar.addWidget(self.increase_btn)
        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.export_btn)
        toolbar.addWidget(self.monitor_count_label)

        toolbar.addStretch()
        toolbar.addWidget(self.theme_btn)

        # Add widgets to main layout
        layout.addLayout(toolbar)
        layout.addWidget(self.text_display)

        self.buttons = [
            self.decrease_btn,
            self.increase_btn,
            self.refresh_btn,
            self.export_btn,
            self.theme_btn,
        ]
        # Connect font size buttons
        self.decrease_btn.clicked.connect(self.decrease_font_size)  # type: ignore
        self.increase_btn.clicked.connect(self.increase_font_size)  # type: ignore
        self.refresh_btn.clicked.connect(self.refresh_monitor_info)  # type: ignore
        self.export_btn.clicked.connect(self.export_info)  # type: ignore
        self.theme_btn.clicked.connect(self.toggle_theme)  # type: ignore

        # Initial refresh
        self.refresh_monitor_info()

    def decrease_font_size(self):
        self.adjust_font_size(-2)

    def increase_font_size(self):
        self.adjust_font_size(2)

    def adjust_font_size(self, delta: int):
        """Adjust the font size by the specified delta"""
        current_size = int(self.font_size_label.text())
        new_size = current_size + delta
        if 8 <= new_size <= 36:
            self.font_size_label.setText(str(new_size))
            font = self.text_display.font()
            font.setPointSize(new_size)
            self.text_display.setFont(font)

    def export_info(self):
        """Export the display information to various file formats"""
        monitor_content = self.text_display.toPlainText()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 修改檔案類型選項，加入 bin 格式
        file_types = "Text Files (*.txt);;" "HTML Files (*.html);;" "All Files (*.*)"

        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "儲存檔案",
            f"EDID_Info_{timestamp}",
            file_types,
        )

        if not filename:  # 用户取消了对话框
            return

        try:
            # 根据选择的文件类型或文件扩展名处理不同格式
            if selected_filter.startswith("Text Files") or filename.lower().endswith(
                ".txt"
            ):
                self._export_as_txt(filename, monitor_content)
            elif selected_filter.startswith("HTML Files") or filename.lower().endswith(
                ".html"
            ):
                self._export_as_html(filename, monitor_content)

            else:
                # 默认导出为文本格式
                self._export_as_txt(filename, monitor_content)

            # 显示成功消息
            QMessageBox.information(
                self, "導出成功", f"EDID信息已成功導出到:\n{filename}"
            )

        except Exception as e:
            # 显示错误消息
            QMessageBox.critical(self, "導出失敗", f"導出文件時發生錯誤:\n{str(e)}")

    def _export_as_txt(self, filename: str, content: str):
        """導出txt格式"""
        # 如果文件名没有扩展名，添加.txt
        if not filename.lower().endswith(".txt"):
            filename += ".txt"

        with open(filename, "w", encoding="utf-8") as f:
            # 加入標題
            f.write("=" * 60 + "\n")
            f.write("EDID 顯示器信息導出\n")
            f.write(f"導出時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            # 寫入主要内容
            f.write(content)

            # 添加文件尾部信息
            f.write("\n\n" + "=" * 60 + "\n")
            f.write("導出完成\n")
            f.write("=" * 60 + "\n")

    def _export_as_html(self, filename: str, content: str):
        """導出HTML格式"""
        if not filename.lower().endswith(".html"):
            filename += ".html"

        html_content = content.replace("\n", "<br>\n").replace(" ", "&nbsp;")

        html_template = f"""<!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EDID 顯示器信息</title>
        <style>
            body {{
                font-family: Inconsolata SemiExpanded;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            h1, h2 {{
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 4px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>EDID 顯示器信息</h1>
                <p class="timestamp">導出時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            <div class="content">
    {html_content}
            </div>
        </div>
    </body>
    </html>"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_template)

    def remove_start_end_lines_specific(self, text: str) -> str:
        """針對特定格式的分隔線進行清理"""
        # 方法3: 針對你的特定格式
        patterns = [
            r"^=+ .* parse started =+$",
            r"^=+ .* parse ended =+$",
            r"^=+ .* parse completed =+$",
            r"^=+.*parse started=+$",
            r"^=+.*parse completed=+$",
        ]

        result = text
        for pattern in patterns:
            result = re.sub(pattern, "", result, flags=re.MULTILINE)

        # 清理多餘的空行
        result = re.sub(r"\n\s*\n", "\n\n", result)
        result = result.strip()

        return result

    def add_titles(self, text: str) -> str:
        """在有內容的分隔線區塊中加入標題"""

        # 定義區塊模式和對應的標題
        section_patterns: List[Dict[str, str]] = [
            {
                "start": "==========edid raw data parse started==========",
                "end": "==========edid raw data parse completed==========",
                "title": "EDID Raw Data",
            },
            {
                "start": "========== video data block parse started ==========",
                "end": "========== video data block parse ended ==========",
                "title": "影像資料區塊 (Video Data Block)",
            },
            {
                "start": "========== audio data block parse started ==========",
                "end": "========== audio data block parse ended ==========",
                "title": "音訊資料區塊 (Audio Data Block)",
            },
            {
                "start": "========== speaker data block parse started ==========",
                "end": "========== speaker data block parse ended ==========",
                "title": "揚聲器配置區塊 (Speaker Data Block)",
            },
            {
                "start": "========== VSDB parse started ==========",
                "end": "========== VSDB parse ended ==========",
                "title": "廠商特定資料區塊 (Vendor Specific Data Block)",
            },
            {
                "start": "========== Colorimetry Data Block parse started ==========",
                "end": "========== Colorimetry Data Block parse completed ==========",
                "title": "HDR 色彩支援區塊 (Colorimetry Data Block)",
            },
            {
                "start": "========== YCbCr 4:2:0 Capability Map parse started ==========",
                "end": "========== YCbCr 4:2:0 Capability Map parse ended ==========",
                "title": "YCbCr 4:2:0 支援區塊",
            },
            {
                "start": "==========DTD or Display Descriptor parse started==========",
                "end": "==========DTD or Display Descriptor parse completed==========",
                "title": "詳細時序描述區塊 (Detailed Timing Descriptor)",
            },
            {
                "start": "==========display id parse started==========",
                "end": "==========display id parse completed==========",
                "title": "顯示器 ID 區塊 (Display ID Block)",
            },
            {
                "start": "==========header parse started==========",
                "end": "==========header parse completed==========",
                "title": "基本顯示器資訊 (Header Information)",
            },
            {
                "start": "==========established timing parse started==========",
                "end": "==========established timing parse completed==========",
                "title": "標準時序區塊 (Established Timing)",
            },
            {
                "start": "==========standard timing parse started==========",
                "end": "==========standard timing parse completed==========",
                "title": "標準時序區塊 (Standard Timing)",
            },
        ]

        for pattern in section_patterns:
            start_pattern: str = re.escape(pattern["start"])
            end_pattern: str = re.escape(pattern["end"])

            # 建立正規表達式來匹配整個區塊
            block_regex: str = f"({start_pattern})(.*?)({end_pattern})"

            def replace_block(match: Match[str]) -> str:
                start_delimiter: str = match.group(1)
                content: str = match.group(2)
                end_delimiter: str = match.group(3)

                # 檢查內容是否只包含空白字符和換行符
                content_stripped: str = content.strip()

                if content_stripped:  # 如果有實際內容
                    # 在開始分隔線後加入標題
                    title_line: str = f"\n【{pattern['title']}】"
                    return start_delimiter + title_line + content + end_delimiter
                else:
                    # 如果沒有內容，保持原樣（之後會被 remove_empty_blocks 移除）
                    return match.group(0)

            # 使用 re.DOTALL 讓 . 也能匹配換行符
            text = re.sub(block_regex, replace_block, text, flags=re.DOTALL)

        return text

    def remove_empty_blocks(self, text: str) -> str:
        """移除所有空的區塊"""

        # 定義所有可能的空區塊模式
        empty_blocks = [
            # Video Data Block
            "========== video data block parse started ==========\n========== video data block parse ended ==========",
            # Audio Data Block
            "========== audio data block parse started ==========\n========== audio data block parse ended ==========",
            # Speaker Data Block
            "========== speaker data block parse started ==========\n========== speaker data block parse ended ==========",
            # VSDB
            "========== VSDB parse started ==========\n========== VSDB parse ended ==========",
            # Colorimetry Data Block
            "========== Colorimetry Data Block parse started ==========\n========== Colorimetry Data Block parse completed ==========",
            # YCbCr 4:2:0 Capability Map
            "========== YCbCr 4:2:0 Capability Map parse started ==========\n========== YCbCr 4:2:0 Capability Map parse ended ==========",
            # DTD or Display Descriptor
            "==========DTD or Display Descriptor parse started==========\n==========DTD or Display Descriptor parse completed==========",
            # Display ID
            "==========display id parse started==========\n==========display id parse completed==========",
            # Header
            "==========header parse started==========\n==========header parse completed==========",
            # Established Timing
            "==========established timing parse started==========\n==========established timing parse completed==========",
            # Standard Timing
            "==========standard timing parse started==========\n==========standard timing parse completed==========",
        ]

        # 逐一移除所有空區塊
        for empty_block in empty_blocks:
            # 處理可能的換行符變化
            variations = [
                empty_block,  # 原始格式
                empty_block + "\n",  # 後面有一個換行
                empty_block + "\n\n",  # 後面有兩個換行
            ]

            for variation in variations:
                text = text.replace(variation, "")

        # 清理多餘的空行（超過兩個連續換行的情況）
        import re

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def format_edid_data(self, data: TotalResult) -> str:
        """將 EDID 資料格式化為類似 format_data.txt 的格式"""
        if not data:
            return "無法讀取顯示器資訊"

        formatted_text: str = ""
        try:
            # Header 資訊
            if (
                "StandardBlockInfo" in data
                and "HeaderInfo" in data["StandardBlockInfo"]
            ):
                header = data["StandardBlockInfo"]["HeaderInfo"]

                formatted_text += "==========header parse started==========\n"

                formatted_text += f"製造商ID        {header.get('MF_id', 'N/A')}\n"
                formatted_text += (
                    f"產品代碼        {header.get('product_code', 'N/A')}\n"
                )
                if header.get("serial_number", "N/A") != "N/A":
                    formatted_text += (
                        f"序列號碼        {header.get('serial_number', 'N/A')}\n"
                    )
                    formatted_text += (
                        f"製造週數        {header.get('MF_week', 'N/A')}\n"
                    )
                    formatted_text += (
                        f"製造年份        {header.get('MF_year', 'N/A')}\n"
                    )
                formatted_text += f"EDID版本        {header.get('version', 'N/A')}\n"
                formatted_text += "==========header parse completed==========\n\n"

            # # Established Timing 資訊(低解析度不具參考價值)
            # if (
            #     "StandardBlockInfo" in data
            #     and "TimingInfo" in data["StandardBlockInfo"]
            # ):
            #     timing = data["StandardBlockInfo"]["TimingInfo"]
            #     formatted_text += (
            #         "==========established timing parse started==========\n"
            #     )

            #     if "Established_1" in timing:
            #         # 先檢查是否有有效的解析度
            #         valid_resolutions = [
            #             est
            #             for est in timing["Established_1"]
            #             if est["resolution"] != "Undefined"
            #         ]

            #         if valid_resolutions:  # 只有在有有效解析度時才加入標題
            #             formatted_text += "第一組標準時序:\n"
            #             for est in valid_resolutions:
            #                 formatted_text += f"{est['resolution']} @ {est['refresh_rate']}Hz ({est['source']})\n"

            #     if "Established_2" in timing:
            #         # 先檢查是否有有效的解析度
            #         valid_resolutions = [
            #             est
            #             for est in timing["Established_2"]
            #             if est["resolution"] != "Undefined"
            #         ]

            #         if valid_resolutions:  # 只有在有有效解析度時才加入標題
            #             formatted_text += "第二組標準時序:\n"
            #             for est in valid_resolutions:
            #                 formatted_text += f"{est['resolution']} @ {est['refresh_rate']}Hz ({est['source']})\n"

            #     formatted_text += (
            #         "==========established timing parse completed==========\n\n"
            #     )

            #     # Standard Timing 資訊
            #     formatted_text += (
            #         "==========standard timing parse started==========\n"
            #     )

            #     if "Standard" in timing:
            #         for std in timing["Standard"]:
            #             if std["h_res"] != "Undefined":
            #                 formatted_text += f"{std['h_res']}x{std['v_res']} @ {std['refresh_rate']}Hz ({std['aspect_ratio']})\n"
            #     formatted_text += (
            #         "==========standard timing parse completed==========\n\n"
            #     )

            # DTD 資訊
            if "StandardBlockInfo" in data and "DTDInfo" in data["StandardBlockInfo"]:
                dtd = data["StandardBlockInfo"]["DTDInfo"]
                formatted_text += (
                    "==========DTD or Display Descriptor parse started==========\n"
                )

                if "perferred_timing" in dtd:
                    formatted_text += f"首選時序解析度: {dtd['perferred_timing']}\n"
                if "dtd_timing" in dtd:
                    valid_timings = [
                        timing for timing in dtd["dtd_timing"] if timing
                    ]  # 過濾掉空值
                    if valid_timings:
                        formatted_text += "時序解析度: "
                        for timing in valid_timings:
                            formatted_text += f"{timing}\n"
                if "dp_descriptor" in dtd:
                    if "display_range_limits" in dtd["dp_descriptor"]:
                        range_limits = dtd["dp_descriptor"]["display_range_limits"][
                            "max_resolution"
                        ]
                        max_rate = dtd["dp_descriptor"]["display_range_limits"][
                            "max_refresh_rate"
                        ]
                        formatted_text += f"最大時序解析度: {range_limits}\n"
                        formatted_text += f"最大垂直更新率: {max_rate}\n"

                    if "ascii_string" in dtd["dp_descriptor"]:
                        ascii_string = dtd["dp_descriptor"]["ascii_string"][
                            "AsciiString"
                        ]
                        formatted_text += f"文字敘述: {ascii_string}\n"

                    if "display_product_name" in dtd["dp_descriptor"]:
                        product_name = dtd["dp_descriptor"]["display_product_name"][
                            "ProductName"
                        ]
                        formatted_text += f"產品名稱: {product_name}\n"

                    if "display_serial_number" in dtd["dp_descriptor"]:
                        serial_number = dtd["dp_descriptor"]["display_serial_number"][
                            "SerialNumber"
                        ]
                        formatted_text += f"序列號碼: {serial_number}\n"
                formatted_text += (
                    "==========DTD or Display Descriptor parse completed==========\n\n"
                )

            # CTA Block 資訊
            if "CTABlockInfo" in data:
                cta = data["CTABlockInfo"]

                # Video Data Block
                formatted_text += (
                    "========== video data block parse started ==========\n"
                )

                if "TagCodeInfo" in cta:
                    for tag in cta["TagCodeInfo"]:
                        if "descriptor" in tag and "VIC" in tag["descriptor"]:
                            # 分割 VIC 資訊並格式化
                            vic_info = tag["descriptor"].split("| ")
                            for vic in vic_info:
                                if vic.strip():
                                    # 每個 VIC 資訊加入換行
                                    formatted_text += f"{vic.strip()}\n"
                            break
                formatted_text += (
                    "========== video data block parse ended ==========\n\n"
                )

                # Audio Data Block
                formatted_text += (
                    "========== audio data block parse started ==========\n"
                )

                for tag in cta.get("TagCodeInfo", []):
                    if "descriptor" in tag and "L-PCM" in tag["descriptor"]:
                        formatted_text += f"{tag['descriptor']}\n"
                        break
                formatted_text += (
                    "========== audio data block parse ended ==========\n\n"
                )

                # Speaker Data Block
                formatted_text += (
                    "========== speaker data block parse started ==========\n"
                )

                for tag in cta.get("TagCodeInfo", []):
                    if "descriptor" in tag and "FL/FR" in tag["descriptor"]:
                        formatted_text += (
                            f"Speaker Configuration: {tag['descriptor']}\n"
                        )
                        break
                formatted_text += (
                    "========== speaker data block parse ended ==========\n\n"
                )

                # VSDB
                formatted_text += "========== VSDB parse started ==========\n"

                for tag in cta.get("TagCodeInfo", []):
                    if "CEC_PA" in tag:
                        formatted_text += f"CEC PA {tag['CEC_PA']}\n"
                        if "res_support" in tag:
                            formatted_text += (
                                f"支援解析度 {tag.get('res_support', '')}\n"
                            )
                        if "color_depths" in tag:
                            formatted_text += (
                                f"位元深度 {tag.get('color_depths', '')}\n"
                            )
                        if "rgb_444_support" in tag:
                            formatted_text += f"{tag.get('rgb_444_support', '')}\n"
                        break
                formatted_text += "========== VSDB parse ended ==========\n\n"

                # HDR 支援
                formatted_text += (
                    "========== Colorimetry Data Block parse started ==========\n"
                )

                for tag in cta.get("TagCodeInfo", []):
                    if "HDR Static Metadata Data Block" in tag:
                        formatted_text += f"{tag['HDR Static Metadata Data Block']}\n"
                        break
                formatted_text += (
                    "========== Colorimetry Data Block parse completed ==========\n\n"
                )

                # YCbCr 4:2:0
                formatted_text += (
                    "========== YCbCr 4:2:0 Capability Map parse started ==========\n"
                )

                for tag in cta.get("TagCodeInfo", []):
                    if "YCbCr 4:2:0 Capability Map Data Block" in tag:

                        formatted_text += (
                            f"{tag['YCbCr 4:2:0 Capability Map Data Block']}\n"
                        )
                        break

                formatted_text += (
                    "========== YCbCr 4:2:0 Capability Map parse ended ==========\n\n"
                )

                # CTA DTD 資訊
                if "DTDInfo" in cta and "dtd_timing" in cta["DTDInfo"]:
                    formatted_text += (
                        "==========DTD or Display Descriptor parse started==========\n"
                    )

                    for timing in cta["DTDInfo"]["dtd_timing"]:
                        formatted_text += f"時序解析度: {timing}\n"
                    formatted_text += "==========DTD or Display Descriptor parse completed==========\n\n"

            # Display ID Block
            if "DisplayIDBlockInfo" in data and "Type_I" in data["DisplayIDBlockInfo"]:
                formatted_text += "==========display id parse started==========\n"

                for timing in data["DisplayIDBlockInfo"]["Type_I"]:
                    formatted_text += f"時序解析度: {timing}\n"
                formatted_text += "==========display id parse completed==========\n"

            if "EDIDRawData" in data:
                formatted_text += "==========edid raw data parse started==========\n"
                formatted_text += f"{data['EDIDRawData']}\n"
                formatted_text += (
                    "==========edid raw data parse completed==========\n\n"
                )

            formatted_text = self.add_titles(formatted_text)
            formatted_text = self.remove_empty_blocks(formatted_text)
            formatted_text = self.remove_start_end_lines_specific(formatted_text)
        except Exception as e:
            formatted_text += f"資料格式化時發生錯誤: {str(e)}\n"
            formatted_text += f"原始資料: {str(data)}"

        return formatted_text

    def update_display(self):
        """更新顯示內容基於選擇的資訊類型"""
        for index in range(len(self.parsed_data_list)):
            self.parsed_data = self.parsed_data_list[index]
            if self.parsed_data:

                content = self.format_edid_data(self.parsed_data)
                self.text_display.append(f"{'='*18}第{index+1}個顯示器資訊{'='*18}")
                self.text_display.append(content)
                self.monitor_count_label.setText(f"目前顯示器數量: {index+1}")
            else:
                self.text_display.clear()
                self.text_display.append("無法讀取顯示器資訊，請確認顯示器連接正常")

        # 更新完內容移動游標到內容的開頭
        self.text_display.moveCursor(QTextCursor.MoveOperation.Start)

    def refresh_monitor_info(self):
        """Refresh monitor information"""
        self.text_display.clear()
        self.text_display.append("正在讀取顯示器資訊...")
        self.text_display.clear()

        try:
            # 調用 EDID 解析器
            self.parsed_data_list = edid_parser()
            self.update_display()

        except Exception as e:
            self.text_display.clear()
            self.text_display.append(f"讀取顯示器資訊時發生錯誤: {str(e)}")

        # 套用主題
        if self.is_dark_mode:
            self.setStyleSheet(self.themes["dark"])
        else:
            self.setStyleSheet(self.themes["light"])

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_mode = not self.is_dark_mode
        theme = "dark" if self.is_dark_mode else "light"

        # 直接使用主題字串
        self.setStyleSheet(self.themes[theme])

        # 更新按鈕文字
        self.theme_btn.setText("切換日間模式" if self.is_dark_mode else "切換夜間模式")


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
