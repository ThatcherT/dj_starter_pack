# This is a command line utility to facilitate the creation of a new Django Project
# Some actions include:
# 1. Rename the Project
# 2. Rename the first App
# 3. Generate more apps as requested
# 3. Remove the Users App if prompted
# 4. Generate a new SECRET_KEY
# 5. Rename numerous things in certain files
# 6. Create passwords for postgres, redis
# 7. Create a new git repo
# 8. Renaming various files throughout the repo based on Project name


import os
import sys
import shutil
import random
import string
import subprocess
import argparse
import json
from pathlib import Path
import re
from utils.secret import generate_secret_key
from utils.general import welcome
from utils.rename import rename_project, rename_app, rename_files

def main():
    """
    This function facilitates command prompt input and calls different utilities after the data is received.
    """
    # set the working directory to the directory of this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    welcome()
    
    

    apps_created = 0
    apps = []
    while True:

        if apps_created:  # code golf
            additional_app_name = input(
                f"2/8. App Name #{apps_created + 1}(Press Enter to Continue...): "
            )
            if not additional_app_name:
                break
            else:
                if additional_app_name in apps:
                    print("App name already exists.")
                    continue
                apps.append(additional_app_name)

        else:
            first_app_name = input("2/8. App Name: ")
            apps.append(first_app_name)
        apps_created += 1
        break
    # copy the app_0 folder to the new project folder
    for app in apps:
        shutil.copytree("./app_0", f"./{app}")
        # project_name replacement rename files
        files_to_change = [f"./{app}/apps.py"]
        for file in files_to_change:
            with open(file, "rw") as f:
                filedata = f.read()
                filedata = filedata.replace("app_0", app)
                filedata = filedata.replace("app0", app)
                f.write(filedata)


if __name__ == "__main__":
    main()
