import monitor
import system_detect
import startup
import os
import ctypes
import os
import json
def read_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
    else:
        return {}

def write_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def set_process_name(name):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(name)


set_process_name("Windows Device Control Manager")

current_directory = os.path.dirname(os.path.abspath(__file__))

config = read_config()

# 检查配置文件中是否已有标记
if config.get('startup_added') != True:
    if system_detect.detect_os() == 'Windows':
        startup.main()
        print("Startup Task Added")
        # 添加标记到配置文件
        config['startup_added'] = True
        write_config(config)
else:
    print("Startup Task Already Added")
monitor.start_monitor()
