import os
import shutil
from utils.general import add_secret_key


def rename_project():
    while True:
        project_name = input("1/8. Project Name: ")
        if project_name:
            # rename project_dir
            shutil.copytree("./assets/dj_starter_pack", f"./{project_name}")
            # TODO: check if ./manage.py exists, if so remove
            shutil.copy("./assets/manage.py", "./manage.py")
            # rename files
            files_to_change = [
                "./manage.py",
                f"./{project_name}/settings.py",
                f"./{project_name}/wsgi.py",
                f"./{project_name}/asgi.py",
                f"./{project_name}/urls.py",
            ]
            for file in files_to_change:
                with open(file, "r") as f:
                    filedata = f.read()
                filedata = filedata.replace("dj_starter_pack", project_name)
                if file == f"./{project_name}/settings.py":
                    filedata = filedata.replace("dsp_key", add_secret_key())
                with open(file, "w") as f:
                    f.write(filedata)
            break
    return project_name


def make_apps(project_name):
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
    # copy the app_0 folder to the new project folder
    for app in apps:
        shutil.copytree("./assets/app_0", f"./{app}")
        # project_name replacement rename files
        files_to_change = [f"./{app}/apps.py"]
        for file in files_to_change:
            with open(file, "r") as f:
                filedata = f.read()
            filedata = filedata.replace("app_0", app)
            # TODO: CamelCaseAppName=
            filedata = filedata.replace("App0", app)
            with open(file, "w") as f:
                f.write(filedata)
    return apps
