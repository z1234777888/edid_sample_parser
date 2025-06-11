import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QComboBox,
)
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from edid_main import main as edid_parser
from datatypes import TotalResult


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_info_type_selection = "完整檢視"  # 保存下拉選單狀態或首次狀態
        self.is_dark_mode = False
        self.parsed_data_list: list[TotalResult] = edid_parser()
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
                    font-family: "Cascadia Mono Light";
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
                    font-family: "Cascadia Mono Light";
                }
            """,
        }

        self.initUI()

    def initUI(self):
        self.setWindowTitle("EDID 解析工具")
        self.setWindowIcon(QIcon(r"branch.ico"))
        self.resize(840, 550)

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
        self.font_size_label = QLabel("12")
        self.font_size_label.setFixedWidth(30)
        self.font_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.increase_btn = QPushButton("+")
        self.increase_btn.setFixedWidth(30)

        # Create text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setAcceptRichText(True)  # 允許富文本

        font = QFont("Cascadia Mono Light", 12)
        self.text_display.setFont(font)

        # Other controls
        self.refresh_btn = QPushButton("重新整理顯示器資訊")
        self.export_btn = QPushButton("匯出資訊")
        self.export_edid_btn = QPushButton("僅匯出EDID")
        self.theme_btn = QPushButton("切換夜間模式")

        self.labels = [font_label, self.font_size_label]
        self.info_type = QComboBox()
        # 添加下拉選單選項
        self.info_type.addItems(
            ["完整檢視", "基本資訊", "時序資訊", "音訊資訊", "HDR支援"]
        )

        # Add controls to toolbar
        toolbar.addWidget(font_label)
        toolbar.addWidget(self.decrease_btn)
        toolbar.addWidget(self.font_size_label)
        toolbar.addWidget(self.increase_btn)
        toolbar.addWidget(self.info_type)
        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.export_btn)
        toolbar.addWidget(self.export_edid_btn)
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
            self.export_edid_btn,
        ]
        # Connect font size buttons
        self.decrease_btn.clicked.connect(self.decrease_font_size)  # type: ignore
        self.increase_btn.clicked.connect(self.increase_font_size)  # type: ignore
        self.refresh_btn.clicked.connect(self.refresh_monitor_info)  # type: ignore
        self.theme_btn.clicked.connect(self.toggle_theme)  # type: ignore
        self.info_type.currentTextChanged.connect(self.update_display)  # type: ignore

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

    def format_edid_data(self, data: TotalResult):
        """將 EDID 資料格式化為類似 format_data.txt 的格式"""
        if not data:
            return "無法讀取顯示器資訊"

        formatted_text = ""

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
                formatted_text += (
                    f"序列號碼        {header.get('serial_number', 'N/A')}\n"
                )
                formatted_text += f"製造週數        {header.get('MF_week', 'N/A')}\n"
                formatted_text += f"製造年份        {header.get('MF_year', 'N/A')}\n"
                formatted_text += f"EDID版本        {header.get('version', 'N/A')}\n"
                formatted_text += "==========header parse completed==========\n\n"

            # Established Timing 資訊
            if (
                "StandardBlockInfo" in data
                and "TimingInfo" in data["StandardBlockInfo"]
            ):
                timing = data["StandardBlockInfo"]["TimingInfo"]

                formatted_text += (
                    "==========established timing parse started==========\n"
                )
                if "Established_1" in timing:
                    # 先檢查是否有有效的解析度
                    valid_resolutions = [
                        est
                        for est in timing["Established_1"]
                        if est["resolution"] != "Undefined"
                    ]

                    if valid_resolutions:  # 只有在有有效解析度時才加入標題
                        formatted_text += "第一組標準時序:\n"
                        for est in valid_resolutions:
                            formatted_text += f"{est['resolution']} @ {est['refresh_rate']}Hz ({est['source']})\n"

                if "Established_2" in timing:
                    # 先檢查是否有有效的解析度
                    valid_resolutions = [
                        est
                        for est in timing["Established_2"]
                        if est["resolution"] != "Undefined"
                    ]

                    if valid_resolutions:  # 只有在有有效解析度時才加入標題
                        formatted_text += "第二組標準時序:\n"
                        for est in valid_resolutions:
                            formatted_text += f"{est['resolution']} @ {est['refresh_rate']}Hz ({est['source']})\n"
                formatted_text += (
                    "==========established timing parse completed==========\n\n"
                )

                # Standard Timing 資訊
                formatted_text += "==========standard timing parse started==========\n"
                if "Standard" in timing:
                    for std in timing["Standard"]:
                        if std["h_res"] != "Undefined":
                            formatted_text += f"{std['h_res']}x{std['v_res']} @ {std['refresh_rate']}Hz ({std['aspect_ratio']})\n"
                formatted_text += (
                    "==========standard timing parse completed==========\n\n"
                )

            # DTD 資訊
            if "StandardBlockInfo" in data and "DTDInfo" in data["StandardBlockInfo"]:
                dtd = data["StandardBlockInfo"]["DTDInfo"]
                formatted_text += (
                    "==========DTD or Display Descriptor parse started==========\n"
                )
                if "perfered_timing" in dtd:
                    formatted_text += f"首選時序解析度: {dtd['perfered_timing']}\n"
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

                    formatted_text += "==========DTD or Display Descriptor parse completed==========\n\n"

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
                        formatted_text += f"支援解析度 {tag.get('res_support', '')}\n"
                        formatted_text += f"位元深度 {tag.get('color_depths', '')}\n"
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

        except Exception as e:
            formatted_text += f"資料格式化時發生錯誤: {str(e)}\n"
            formatted_text += f"原始資料: {str(data)}"

        return formatted_text

    def get_filtered_display(self, info_type: str):
        """根據選擇的資訊類型過濾顯示內容"""
        if not self.parsed_data:
            return "無可用資料"

        if info_type == "完整檢視":
            return self.format_edid_data(self.parsed_data)
        # elif info_type == "基本資訊":
        #     return self.get_basic_info()
        # elif info_type == "時序資訊":
        #     return self.get_timing_info()
        # elif info_type == "音訊資訊":
        #     return self.get_audio_info()
        # elif info_type == "HDR支援":
        #     return self.get_hdr_info()
        else:
            return self.format_edid_data(self.parsed_data)

    def get_basic_info(self):
        """取得基本資訊"""
        if not self.parsed_data:
            return "無可用資料"

        info = ""
        try:
            # Header 資訊
            if (
                "StandardBlockInfo" in self.parsed_data
                and "HeaderInfo" in self.parsed_data["StandardBlockInfo"]
            ):
                header = self.parsed_data["StandardBlockInfo"]["HeaderInfo"]
                info += "==========基本顯示器資訊==========\n"
                info += f"製造商: {header.get('MF_id', 'N/A')}\n"
                info += f"產品代碼: {header.get('product_code', 'N/A')}\n"
                info += f"序列號碼: {header.get('serial_number', 'N/A')}\n"
                info += f"製造日期: {header.get('MF_year', 'N/A')}年第{header.get('MF_week', 'N/A')}週\n"
                info += f"EDID版本: {header.get('version', 'N/A')}\n"

            # 產品名稱 (從 DTD 取得)
            if (
                "StandardBlockInfo" in self.parsed_data
                and "DTDInfo" in self.parsed_data["StandardBlockInfo"]
            ):
                dtd = self.parsed_data["StandardBlockInfo"]["DTDInfo"]
                if "dp_descriptor" in dtd and "SerialNumber" in dtd["dp_descriptor"]:
                    info += f"序列號碼: {dtd['dp_descriptor']['SerialNumber']}\n"
        except Exception as e:
            info += f"取得基本資訊時發生錯誤: {str(e)}"

        return info

    def get_timing_info(self):
        """取得時序資訊"""
        if not self.parsed_data:
            return "無可用資料"

        info = "==========時序解析度資訊==========\n"
        try:
            # 首選時序
            if (
                "StandardBlockInfo" in self.parsed_data
                and "DTDInfo" in self.parsed_data["StandardBlockInfo"]
            ):
                dtd = self.parsed_data["StandardBlockInfo"]["DTDInfo"]
                if "perfered_timing" in dtd:
                    info += f"首選時序: {dtd['perfered_timing']}\n"

            # Display ID 時序
            if (
                "DisplayIDBlockInfo" in self.parsed_data
                and "Type_I" in self.parsed_data["DisplayIDBlockInfo"]
            ):
                info += "\n高更新率時序:\n"
                for timing in self.parsed_data["DisplayIDBlockInfo"]["Type_I"]:
                    info += f"  {timing}\n"

            # CTA 時序
            if (
                "CTABlockInfo" in self.parsed_data
                and "DTDInfo" in self.parsed_data["CTABlockInfo"]
            ):
                cta_dtd = self.parsed_data["CTABlockInfo"]["DTDInfo"]
                if "dtd_timing" in cta_dtd:
                    info += "\n其他支援時序:\n"
                    for timing in cta_dtd["dtd_timing"]:
                        info += f"  {timing}\n"

        except Exception as e:
            info += f"取得時序資訊時發生錯誤: {str(e)}"

        return info

    def get_audio_info(self):
        """取得音訊資訊"""
        if not self.parsed_data:
            return "無可用資料"

        info = "==========音訊支援資訊==========\n"
        try:
            if "CTABlockInfo" in self.parsed_data:
                cta = self.parsed_data["CTABlockInfo"]
                for tag in cta.get("TagCodeInfo", []):
                    if "descriptor" in tag and "L-PCM" in tag["descriptor"]:
                        info += f"音訊格式: {tag['descriptor']}\n"
                    if "descriptor" in tag and "FL/FR" in tag["descriptor"]:
                        info += f"喇叭配置: {tag['descriptor']}\n"
        except Exception as e:
            info += f"取得音訊資訊時發生錯誤: {str(e)}"

        return info

    def get_hdr_info(self):
        """取得 HDR 支援資訊"""
        if not self.parsed_data:
            return "無可用資料"

        info = "==========HDR 支援資訊==========\n"
        try:
            if "CTABlockInfo" in self.parsed_data:
                cta = self.parsed_data["CTABlockInfo"]
                for tag in cta.get("TagCodeInfo", []):
                    if "HDR Static Metadata Data Block" in tag:
                        info += f"{tag['HDR Static Metadata Data Block']}\n"
                    if "YCbCr 4:2:0 Capability Map Data Block" in tag:
                        info += f"{tag['YCbCr 4:2:0 Capability Map Data Block']}\n"
                    if "color_depths" in tag:
                        info += f"位元深度支援: {tag['color_depths']}\n"
                    if "rgb_444_support" in tag:
                        info += f"色彩格式: {tag['rgb_444_support']}\n"
        except Exception as e:
            info += f"取得HDR資訊時發生錯誤: {str(e)}"

        return info

    def update_display(self):
        """更新顯示內容基於選擇的資訊類型"""
        for index in range(len(self.parsed_data_list)):
            self.parsed_data = self.parsed_data_list[index]
            if self.parsed_data:
                # 根據當前選擇的資訊類型顯示內容
                selected_type = self.info_type.currentText()
                content = self.get_filtered_display(selected_type)
                self.text_display.append(f"{'='*32}第{index+1}個顯示器資訊{'='*32}")
                self.text_display.append(content)
            else:
                self.text_display.clear()
                self.text_display.append("無法讀取顯示器資訊，請確認顯示器連接正常")

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
