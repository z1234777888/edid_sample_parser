import PyInstaller.__main__
import os


def create_exe():
    # 取得圖示檔案的絕對路徑
    icon_path = os.path.abspath("branch.ico")  # 圖檔副檔名為ico
    # 定義 PyInstaller 參數
    args = [
        "pyqt_main.py",  # GUI介面主程式
        "--onefile",  # 產生單一執行檔
        "--noconsole",  # 不顯示控制台視窗
        "--clean",  # 清除 PyInstaller 快取
        "--name=簡約版EDID讀取器 V1.0",  # 轉為執行檔後的名稱
        "--icon=" + icon_path,  # 使用圖示
        "--add-data=edid_main.py;.",  # EDID 主要程式
        "--add-data=datatypes.py;.",  # 數值型態定義
        "--add-data=monitor_info.py;.",  # 監視器資訊
        "--add-data=block_map_classify.py;.",  # EDID 區塊分類
        "--add-data=parse_cta_extension.py;.",  # EDID CTA擴充區塊解析
        "--add-data=parse_displayid.py;.",  # EDID DP區塊解析
        "--add-data=parse_standard.py;.",  # EDID 標準區塊解析
        "--add-data=validator.py;.",  # EDID 基礎驗證(Header)
        "--add-data=vic_to_resolution.py;.",  # vic 轉換解析度 table
        "--add-data=vic.py;.",  # VIC定義 table
        "--uac-admin",  # 要求管理員權限
        "--windowed",  # GUI 應用程式設定
    ]

    # 加入 PyQt6 相關依賴
    args.extend(
        [
            "--hidden-import=PyQt6",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=PyQt6.sip",
        ]
    )

    # 執行 PyInstaller
    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    create_exe()
