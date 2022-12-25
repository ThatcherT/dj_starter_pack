import random
import os
import shutil


class Project:
    "This small class facilitates the manipulation of assets to output a custom built project"

    def __init__(self):
        self.asset_files = ["assets", "utils", ".gitignore", "README.md", "bang.py", ".git"]
        pass

    def welcome(self):
        welcome_messages = [
            "LGTM!",
            "This project will be the one to change the world.",
            "You are a great developer.",
            "Python is my love language.",
            "Don't forget to drink water.",
            "Remember your ambitions.",
            "Starting things is fun!",
        ]
        print(random.choice(welcome_messages))

    def _unbang(self):
        "removes created assets in the project"
        files = os.listdir(".")
        for file in files:
            if file not in self.asset_files:
                try:
                    os.remove(file)
                except:
                    print('Reminder to make this work for folders..')

    def _add_secret_key(self):
        "open .env, generate SECRET_KEY, write to .env, return secret"
        with open("./.env", "w") as f:
            secret_key = secrets.token_urlsafe()
            # write
            dj_secret = f"DJANGO_SECRET_KEY={secret_key}"
            f.write(dj_secret)
        return secret_key

    def rename_project(self):
        while True:
            project_name = input("1/8. Project Name: ")
            if project_name == "-":
                self._unbang()
                exit()
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
                        filedata = filedata.replace("dsp_key", self._add_secret_key())
                    with open(file, "w") as f:
                        f.write(filedata)
                break
        self.project_name = project_name

    def make_apps(self):
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
        self.apps = apps
