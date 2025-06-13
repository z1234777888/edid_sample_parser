# 步驟一：生成內嵌字體文件的工具
# 運行這個腳本來生成 embedded_fonts.py

import base64
import os

def generate_embedded_font_file():
    """生成包含內嵌字體的 Python 文件"""
    
    # 字體文件路径
    font_path = "fonts/INCONSOLATA_SEMIEXPANDED-REGULAR.ttf"
    
    if not os.path.exists(font_path):
        print(f"字體文件不存在: {font_path}")
        return
    
    # 讀取字體文件並轉換為 Base64
    with open(font_path, "rb") as font_file:
        font_data = font_file.read()
        encoded_font = base64.b64encode(font_data).decode('utf-8')
    
    # 生成 Python 文件內容
    python_code = f'''"""
內嵌字體文件
自動生成，請勿手動編輯
"""

import base64
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QFontDatabase

# Base64 編碼的字體數據
INCONSOLATA_FONT_DATA = """\\
{encoded_font}
"""

def load_embedded_fonts():
    """載入內嵌字體並返回字體家族名稱"""
    try:
        # 解碼 Base64 數據
        font_bytes = base64.b64decode(INCONSOLATA_FONT_DATA)
        
        # 創建 QByteArray
        byte_array = QByteArray(font_bytes)
        
        # 載入字體
        font_id = QFontDatabase.addApplicationFontFromData(byte_array)
        
        if font_id != -1:
            # 取得字體家族名稱
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                print(f"成功載入內嵌字體: {{font_families[0]}}")
                return font_families[0]
        
        print("載入內嵌字體失敗")
        return None
    
    except Exception as e:
        print(f"載入內嵌字體時發生錯誤: {{e}}")
        return None
'''
    
    # 寫入文件
    with open("embedded_fonts.py", "w", encoding="utf-8") as output_file:
        output_file.write(python_code)
    
    print("已生成 embedded_fonts.py")
    print(f"原始字體文件大小: {len(font_data):,} bytes")
    print(f"Base64 編碼後大小: {len(encoded_font):,} characters")

# 執行生成
if __name__ == "__main__":
    generate_embedded_font_file()

# ================================
# 步驟二：在你的 main.py 中使用內嵌字體
# ================================

"""
在你的 main.py 中這樣使用：

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from embedded_fonts import load_embedded_fonts  # 導入內嵌字體

def main():
    app = QApplication(sys.argv)
    
    # 載入內嵌字體
    font_family = load_embedded_fonts()
    
    if font_family:
        # 成功載入，設置字體
        font = QFont()
        font.setFamilies([font_family, "Consolas", "monospace"])  # 主要+備用字體
        font.setPointSize(14)
        app.setFont(font)
    else:
        # 載入失敗，使用系統字體
        app.setFont(QFont("Consolas", 14))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
"""

# ================================
# 更簡潔的版本
# ================================

"""
如果你只想要最簡潔的版本：

def main():
    app = QApplication(sys.argv)
    
    # 一行載入內嵌字體
    font_family = load_embedded_fonts()
    app.setFont(QFont(font_family or "Consolas", 14))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
"""