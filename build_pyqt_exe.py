import PyInstaller.__main__
import os


def create_exe_with_better_optimization():
    """
    優化版本：加入更多優化選項
    """
    icon_path = os.path.abspath("icon/branch.ico")

    args = [
        "pyqt_main.py",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name=EDID解析器 v1.1.0",
        "--icon=" + icon_path,
        # 加入所有相關的 Python 檔案
        "--add-data=edid_main.py;.",
        "--add-data=datatypes.py;.",
        "--add-data=monitor_info.py;.",
        "--add-data=block_map_classify.py;.",
        "--add-data=parser;parser",
        "--add-data=validator.py;.",
        "--add-data=vic_data;vic_data",
        "--add-data=fonts/embedded_fonts.py;fonts",
        # 權限和視窗設定
        "--uac-admin",
        "--windowed",
        # 優化選項
        "--optimize=2",  # Python 字節碼優化
        "--noupx",  # 不使用 UPX 壓縮（可能導致防毒軟體誤報）
    ]

    # PyQt6 相關依賴
    args.extend(
        [
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
        ]
    )

    PyInstaller.__main__.run(args)


if __name__ == "__main__":

    create_exe_with_better_optimization()
