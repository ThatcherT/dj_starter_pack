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
import argparse


def main():
    """This function facilitates command prompt input and calls different utilities after the data is received."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    proj = Project()
    proj.welcome()
    proj.rename_project()
    proj.create_apps()
    proj.set_services()
    proj.projectify()

    print("Successfully created project: ", proj.project_name)
    print(f"With services: {', '.join([service for service in proj.services])}")
    print(
        "If you are satisified, delete the dj_starter_pack assets with `python bang.py --destroy`"
    )
    print(
        "If you are not satisfied, delete the created resources with `python bang.py --unbang`"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--destroy", help="Destroy the dj_starter_pack assets", action="store_true"
    )
    parser.add_argument(
        "--unbang", help="Remove created resources.", action="store_true"
    )
    args = parser.parse_args()
    if args.destroy:
        print("Destroying the project.")
        proj = Project()
        proj.destroy()
        print("Thanks for using dj_starter_pack.")
    elif args.unbang:
        print("Removing created resources.")
        proj = Project()
        proj.unbang()
        print("Run python bang.py to start over.")
    else:
        main()
