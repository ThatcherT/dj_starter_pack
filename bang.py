# This is a command line utility to facilitate the creation of a new Django Project
# Some actions include:
# 1. Initialize Project from assets
# 2. Generate a new SECRET_KEY add to .env
# 2. Generate Apps from assets
# 3. Remove the Users App if prompted
# 6. Create passwords for postgres, redis
# 8. Renaming various files throughout the repo based on Project name


import os
from utils.main import Project


def main():
    """
    This function facilitates command prompt input and calls different utilities after the data is received.
    """
    # set the working directory to the directory of this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    proj = Project()
    
    proj.welcome()

    proj.rename_project()

    proj.create_apps()

    proj.set_services()

    proj.projectify()
    

    print("Initialize pre-commit with command pre-commit --install .")

    # TODO: remove_assets_and_utils


if __name__ == "__main__":
    main()
