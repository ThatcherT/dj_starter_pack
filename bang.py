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
from utils.secret import generate_secret_key
from utils.general import welcome
from utils.rename import rename_project, make_apps


def main():
    """
    This function facilitates command prompt input and calls different utilities after the data is received.
    """
    # set the working directory to the directory of this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    welcome()

    project_name = rename_project()

    app_lst = make_apps(project_name)

    # TODO: remove_assets_and_utils


if __name__ == "__main__":
    main()
