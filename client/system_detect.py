import platform

def detect_os():
    os_type = platform.system()
    if os_type == "Windows":
        print("This is a Windows system.")
        # Windows specific code here
    elif os_type == "Darwin":
        print("This is a macOS system.")
        # macOS specific code here
    elif os_type == "Linux":
        print("This is a Linux system.")
        # Linux specific code here
    else:
        print(f"Unsupported OS: {os_type}")
    return os_type

if __name__ == "__main__":
    detect_os()
