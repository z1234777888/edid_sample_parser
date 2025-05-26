from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import ctypes
import winreg


class DISPLAY_DEVICE(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.c_ulong),
        ("DeviceName", ctypes.c_wchar * 32),
        ("DeviceString", ctypes.c_wchar * 128),
        ("StateFlags", ctypes.c_ulong),
        ("DeviceID", ctypes.c_wchar * 128),
        ("DeviceKey", ctypes.c_wchar * 128),
    ]


@dataclass
class MonitorInfo:
    registry_paths: List[Tuple[str, str]]
    active_monitors: List[Dict[str, str]]


class MonitorManager:
    @staticmethod
    def get_monitor_registry_paths() -> List[Tuple[str, str]]:
        """搜尋所有具有 EDID 數據的顯示器註冊表路徑"""
        print("正在搜尋所有顯示器註冊表路徑...")
        paths: List[Tuple[str, str]] = []
        try:
            base_path = r"SYSTEM\CurrentControlSet\Enum\DISPLAY"
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                base_path,
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
            ) as key:

                for i in range(winreg.QueryInfoKey(key)[0]):
                    manufacturer = winreg.EnumKey(key, i)
                    mfg_path = f"{base_path}\\{manufacturer}"
                    try:
                        with winreg.OpenKey(
                            winreg.HKEY_LOCAL_MACHINE,
                            mfg_path,
                            0,
                            winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
                        ) as mfg_key:

                            for j in range(winreg.QueryInfoKey(mfg_key)[0]):
                                instance = winreg.EnumKey(mfg_key, j)
                                params_path = (
                                    f"{mfg_path}\\{instance}\\Device Parameters"
                                )

                                try:
                                    with winreg.OpenKey(
                                        winreg.HKEY_LOCAL_MACHINE,
                                        params_path,
                                        0,
                                        winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
                                    ) as params_key:
                                        if winreg.QueryValueEx(params_key, "EDID")[0]:
                                            paths.append((manufacturer, instance))
                                except WindowsError:
                                    continue
                    except WindowsError:
                        continue
            return paths
        except Exception as e:
            print(f"搜尋註冊表路徑時發生錯誤: {str(e)}")
            return []

    @staticmethod
    def get_physical_monitors() -> List[Dict[str, str]]:
        """獲取當前實際連接的顯示器資訊"""
        print("正在識別當前活動顯示器...")
        monitors: List[Dict[str, str]] = []

        try:
            i = 0
            display_device = DISPLAY_DEVICE()
            display_device.cb = ctypes.sizeof(display_device)

            while ctypes.windll.user32.EnumDisplayDevicesW(
                None, i, ctypes.byref(display_device), 0
            ):
                if display_device.StateFlags & 0x1:  # DISPLAY_DEVICE_ACTIVE
                    monitor_device = DISPLAY_DEVICE()
                    monitor_device.cb = ctypes.sizeof(monitor_device)
                    if ctypes.windll.user32.EnumDisplayDevicesW(
                        display_device.DeviceName, 0, ctypes.byref(monitor_device), 0
                    ):
                        monitor_id = monitor_device.DeviceID.split("\\")[1]

                        monitor_info = {
                            "name": display_device.DeviceString,
                            "model": monitor_id,
                            "device_id": monitor_device.DeviceID,
                        }
                        monitors.append(monitor_info)
                i += 1

            return monitors

        except Exception as e:
            print(f"獲取顯示器資訊時發生錯誤: {str(e)}")
            return []

    def get_monitor_edid(self, manufacturer: str, instance: str) -> Optional[bytes]:
        """從註冊表中獲取指定顯示器的 EDID 數據"""
        try:
            registry_path = f"SYSTEM\\CurrentControlSet\\Enum\\DISPLAY\\{manufacturer}\\{instance}\\Device Parameters"

            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                registry_path,
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
            ) as key:
                return winreg.QueryValueEx(key, "EDID")[0]

        except WindowsError:
            return None

    def monitor_read(self) -> MonitorInfo:
        try:
            registry_paths = self.get_monitor_registry_paths()
            active_monitors = self.get_physical_monitors()

            return MonitorInfo(
                registry_paths=registry_paths, active_monitors=active_monitors
            )
        except Exception as e:
            print(f"獲取顯示器資訊時發生錯誤: {str(e)}")
        return MonitorInfo(registry_paths=[], active_monitors=[])

    def display_monitor_info(
        self,
        index: int,
        monitor: Dict[str, str],
        registry_paths: List[Tuple[str, str]],
    ) -> Optional[bytes]:
        print(f"{'='*32}第{index}個顯示器資訊{'='*32}")
        print(f"顯示器名稱: {monitor['name']}")
        print(f"顯示器型號: {monitor['model']}")
        edid_data: Optional[bytes] = None
        found_edid = False
        for manufacturer, instance in registry_paths:
            if manufacturer in monitor["model"]:
                edid_data = self.get_monitor_edid(manufacturer, instance)
                if edid_data:
                    found_edid = True
                    break

        if not found_edid:
            print("EDID 數據: 未找到")

        return edid_data
