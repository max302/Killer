import json
import os
import re
import subprocess

import fcntl

from killer.killer_base import KillerBase

BT_MAC_REGEX = re.compile("(?:[0-9a-fA-F]:?){12}")
BT_NAME_REGEX = re.compile("[0-9A-Za-z ]+(?=\s\()")
BT_CONNECTED_REGEX = re.compile("(Connected: [0-1])")
USB_ID_REGEX = re.compile("(idProduct)\s=\s0x(\w+)")

class KillerBSD(KillerBase):
    def __init__(self, config_path: str = None, debug: bool = False):
        super().__init__(config_path, debug)

    def detect_bt(self): #NOT DONE
        return 0;

    def detect_usb(self):
        ids = re.findall(USB_ID_REGEX, subprocess.check_output("usbconfig dump_device_desc",
                                                                shell=False).decode())
        if self.DEBUG:
            print("USB:")
            print(', '.join(ids))
            print()
        else:
            for each_device in ids:
                if each_device not in json.loads(self.config['linux']['USB_ID_WHITELIST']):
                    self.kill_the_system('USB Allowed Whitelist')
            for device in json.loads(self.config['linux']['USB_CONNECTED_WHITELIST']):
                if device not in ids:
                    self.kill_the_system('USB Connected Whitelist')

    def detect_ac(self):  #NOT DONE
        return 0

    def detect_battery(self): #NOT DONE
        return 0

    def detect_tray(self): #NOT DONE
        return 0;

    def detect_ethernet(self): #NOT DONE
        return 0;

    def kill_the_system(self, warning: str):
        super().kill_the_system(warning)
        subprocess.Popen(["/sbin/poweroff", "-f"])
