import PyInstaller.__main__
import os


def create_exe():
    # 如果使用內嵌圖示，就不需要指定 icon 路徑了
    # 但如果你還是想在打包時使用外部圖示檔案作為執行檔圖示，可以保留
    icon_path = os.path.abspath("branch.ico")  # 執行檔本身的圖示

    # 定義 PyInstaller 參數
    args = [
        "pyqt_main.py",  # GUI介面主程式
        "--onefile",  # 產生單一執行檔
        "--noconsole",  # 不顯示控制台視窗
        "--clean",  # 清除 PyInstaller 快取
        "--name=簡約版EDID讀取器 V1.0",  # 轉為執行檔後的名稱
        "--icon=" + icon_path,  # 執行檔本身的圖示（可選）
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


def create_exe_without_external_icon():
    """
    如果完全使用內嵌圖示，不需要外部圖示檔案的版本
    """
    args = [
        "pyqt_main.py",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name=簡約版EDID讀取器 V1.0",
        # 移除 --icon 參數，因為不需要外部圖示檔案
        "--add-data=edid_main.py;.",
        "--add-data=datatypes.py;.",
        "--add-data=monitor_info.py;.",
        "--add-data=block_map_classify.py;.",
        "--add-data=parse_cta_extension.py;.",
        "--add-data=parse_displayid.py;.",
        "--add-data=parse_standard.py;.",
        "--add-data=validator.py;.",
        "--add-data=vic_to_resolution.py;.",
        "--add-data=vic.py;.",
        "--uac-admin",
        "--windowed",
    ]

    args.extend(
        [
            "--hidden-import=PyQt6",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=PyQt6.sip",
        ]
    )

    PyInstaller.__main__.run(args)


def create_exe_with_better_optimization():
    """
    優化版本：加入更多優化選項
    """
    icon_path = os.path.abspath("branch.ico")

    args = [
        "pyqt_main.py",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name=簡約版EDID讀取器 V1.0",
        "--icon=" + icon_path,
        # 加入所有相關的 Python 檔案
        "--add-data=edid_main.py;.",
        "--add-data=datatypes.py;.",
        "--add-data=monitor_info.py;.",
        "--add-data=block_map_classify.py;.",
        "--add-data=parse_cta_extension.py;.",
        "--add-data=parse_displayid.py;.",
        "--add-data=parse_standard.py;.",
        "--add-data=validator.py;.",
        "--add-data=vic_to_resolution.py;.",
        "--add-data=vic.py;.",
        # 權限和視窗設定
        "--uac-admin",
        "--windowed",
        # 優化選項
        # "--optimize=2",  # Python 字節碼優化
        # "--strip",  # 移除除錯符號
        "--noupx",  # 不使用 UPX 壓縮（可能導致防毒軟體誤報）
    ]

    # PyQt6 相關依賴
    args.extend(
        [
            "--hidden-import=PyQt6",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=PyQt6.sip",
        ]
    )

    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    print("選擇打包方式:")
    print("1. 使用外部圖示檔案（原版）")
    print("2. 不使用外部圖示檔案（純內嵌）")
    print("3. 優化版本")

    choice = input("請選擇 (1/2/3): ").strip()

    if choice == "1":
        create_exe()
    elif choice == "2":
        create_exe_without_external_icon()
    elif choice == "3":
        create_exe_with_better_optimization()
    else:
        print("使用預設方式...")
        create_exe()
