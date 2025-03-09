import os
import subprocess
import sys

HOSTNAME = "192.168.4.104"
USERNAME = "ben"
SOURCE_PATH = "/home/ben/dev/staff_of_observability"
INCLUDED_FOLDERS = ["python_client", "service"]
REMOTE_PATH = "/home/ben/dev/staff_of_observability"
RESTART_SERVICE = True if "--restart" in sys.argv else False

# Copy all included folders in the source path to the remote path, maintain the folder structure
for folder in INCLUDED_FOLDERS:
    print(f"Copying {folder} to {HOSTNAME}:{REMOTE_PATH}")
    subprocess.run(["scp", "-r", os.path.join(SOURCE_PATH, folder), f"{USERNAME}@{HOSTNAME}:{os.path.join(REMOTE_PATH, folder)}"])
    # Define shortcuts for targets
    TARGETS = {
        "pi_5": "192.168.4.99",
        "staff_of_o11y_zero2": "192.168.4.104"
    }

    # Function to get hostname from target shortcut
    def get_hostname(target):
        return TARGETS.get(target, target)

    # Function to get included folders from user input
    def get_included_folders():
        folders = input("Enter the folders to include (comma-separated): ")
        return [folder.strip() for folder in folders.split(",")]

    # Function to get remote path from user input
    def get_remote_path():
        return input("Enter the remote path: ")

    # Get target from user input
    target = input("Enter the target (e.g., pi_5, staff_of_o11y_zero2): ")
    HOSTNAME = get_hostname(target)

    # Get included folders and remote path from user input
    INCLUDED_FOLDERS = get_included_folders()
    REMOTE_PATH = get_remote_path()

    # Copy all included folders in the source path to the remote path, maintain the folder structure
    for folder in INCLUDED_FOLDERS:
        print(f"Copying {folder} to {HOSTNAME}:{REMOTE_PATH}")
        subprocess.run(["scp", "-r", os.path.join(SOURCE_PATH, folder), f"{USERNAME}@{HOSTNAME}:{os.path.join(REMOTE_PATH, folder)}"])

    # Restart service if needed
    if RESTART_SERVICE:
        print("Restarting service...")
        subprocess.run(["ssh", f"{USERNAME}@{HOSTNAME}", "sudo systemctl restart your_service_name"])