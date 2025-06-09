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

# fonts
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_info_type_selection = "完整檢視"  # 保存下拉選單狀態或首次狀態
        self.is_dark_mode = False
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

    def refresh_monitor_info(self):
        """Refresh monitor information in a separate thread"""
        self.text_display.clear()
        self.text_display.append("正在讀取顯示器資訊...")
        if self.is_dark_mode is True:
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
