import os
import sys
import subprocess
from pathlib import Path

class CloudGuard:
    def __init__(self):
        self.shortcuts_dir = Path.home() / "Desktop" / "Shortcuts"
        self.startup_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure that the shortcuts and startup directories exist."""
        if not self.shortcuts_dir.exists():
            self.shortcuts_dir.mkdir(parents=True)
        if not self.startup_dir.exists():
            self.startup_dir.mkdir(parents=True)

    def create_shortcut(self, target_path, shortcut_name):
        """Create a shortcut for the target application on the desktop."""
        shortcut_path = self.shortcuts_dir / f"{shortcut_name}.lnk"
        if not shortcut_path.exists():
            command = f'powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut(\'{shortcut_path}\');$s.TargetPath=\'{target_path}\';$s.Save()"'
            subprocess.run(command, shell=True)
            print(f"Shortcut created: {shortcut_path}")
        else:
            print(f"Shortcut already exists: {shortcut_path}")

    def add_to_startup(self, app_name, app_path):
        """Add an application to the startup configuration."""
        startup_path = self.startup_dir / f"{app_name}.lnk"
        if not startup_path.exists():
            command = f'powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut(\'{startup_path}\');$s.TargetPath=\'{app_path}\';$s.Save()"'
            subprocess.run(command, shell=True)
            print(f"Added to startup: {startup_path}")
        else:
            print(f"Application already in startup: {startup_path}")

    def remove_from_startup(self, app_name):
        """Remove an application from the startup configuration."""
        startup_path = self.startup_dir / f"{app_name}.lnk"
        if startup_path.exists():
            startup_path.unlink()
            print(f"Removed from startup: {startup_path}")
        else:
            print(f"Application not found in startup: {startup_path}")

    def list_startup_items(self):
        """List all applications in the startup configuration."""
        print("Startup Applications:")
        for item in self.startup_dir.iterdir():
            print(item.stem)

def main():
    cg = CloudGuard()
    while True:
        print("\nCloudGuard - Application Management")
        print("1. Create Shortcut")
        print("2. Add to Startup")
        print("3. Remove from Startup")
        print("4. List Startup Applications")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            target_path = input("Enter the full path of the application: ")
            shortcut_name = input("Enter the shortcut name: ")
            cg.create_shortcut(target_path, shortcut_name)
        elif choice == '2':
            app_name = input("Enter the application name: ")
            app_path = input("Enter the full path of the application: ")
            cg.add_to_startup(app_name, app_path)
        elif choice == '3':
            app_name = input("Enter the application name to remove from startup: ")
            cg.remove_from_startup(app_name)
        elif choice == '4':
            cg.list_startup_items()
        elif choice == '5':
            sys.exit("Exiting CloudGuard.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()