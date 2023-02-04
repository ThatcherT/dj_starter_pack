from re import sub
import random
import os
import shutil
import secrets
from utils.django_settings_config import EMAIL, REDIS_CACHE, RQ_SCHEDULER
from utils.compose_aggregator import aggregate
import time

# TODO: import something for emojis in the terminal
# TODO: import something for colors in the terminal


class Project:
    "This small class facilitates the manipulation of assets to output a custom built project template"

    def __init__(self):
        self.asset_files = [
            ".pre-commit-config.yaml",
            "assets",
            "utils",
            ".gitignore",
            "README.md",
            "bang.py",
            ".git",
        ]
        self.services = ["nginx", "postgres", "django"]
        self.site_name = ""
        self.service_settings = []
        self.project_name = ""
        self.apps = []
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

    def unbang(self):
        "removes created assets in the project"
        # iterate through the root level directory
        for file in os.listdir():
            if file not in self.asset_files:
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)

    def rename_project(self):
        while True:
            self.project_name = input("1/8. Project Name: ")
            if self.project_name:
                break

    def create_apps(self):
        apps_created = 0
        while True:
            if apps_created:  # code golf
                additional_app_name = input(
                    f"2/8. App Name #{apps_created + 1}(Press Enter to Continue...): "
                )
                if not additional_app_name:
                    break
                else:
                    if additional_app_name in self.apps:
                        print("App name already exists.")
                        continue
                    self.apps.append(additional_app_name)

            else:
                while True:
                    first_app_name = input("2/8. App Name: ")
                    if first_app_name:
                        self.apps.append(first_app_name)
                        break
            apps_created += 1

    def set_services(self):
        redis = input("4/8. Redis? (y/n): ")
        if redis == "y":
            self.services.append("redis")
            redis_cache = input("5/8. Use Redis as a Cache? (y/n): ")
            if redis_cache == "y":
                self.service_settings.append(REDIS_CACHE)
                pass
            rq_scheduler = input("6/8. Use Redis as scheduler? (y/n): ")
            if rq_scheduler == "y":
                self.services.append("scheduler")
                self.service_settings.append(RQ_SCHEDULER)
        email = input("7/8. Email? (y/n): ")
        if email == "y":
            self.service_settings.append(EMAIL)

    def _makefile(self):
        """Build project Makefile Replace dj_starter_kit makefile with project Makefile"""
        # TODO:

    def _nginx(self):
        """Copies nginx.conf to project root, modifies file with updated vars"""
        # read in ./assets/nginx/local/nginx.conf
        with open("./assets/nginx/local/nginx.conf", "r") as f:
            nginx_data_local = f.read()
        if not self.site_name:
            self.site_name = input("3/8. Site Name: ")
        # replace vars
        nginx_data_local = nginx_data_local.replace("$PROJECT_NAME", self.project_name)
        nginx_data_local = nginx_data_local.replace("$SITE_NAME", self.site_name)
        with open("./assets/nginx/prod/nginx.conf", "r") as f:
            nginx_data_prod = f.read()
        # replace vars
        nginx_data_prod = nginx_data_prod.replace("$PROJECT_NAME", self.project_name)
        nginx_data_prod = nginx_data_prod.replace("$SITE_NAME", self.site_name)

        # create folders
        os.mkdir("./nginx")
        os.mkdir("./nginx/local")
        os.mkdir("./nginx/prod")
        # write to ./nginx/local/nginx.conf
        with open("./nginx/local/nginx.conf", "w") as f:
            f.write(nginx_data_local)
        # write to ./nginx/prod/nginx.conf
        with open("./nginx/prod/nginx.conf", "w") as f:
            f.write(nginx_data_prod)

    def _docker(self):
        """Copies Dockerfile to project root, modifies file with updated vars"""
        # read in ./assets/django/Dockerfile
        with open("./assets/django/Dockerfile", "r") as f:
            docker_data = f.read()
        # replace $PROJECT_NAME with self.project_name
        docker_data = docker_data.replace("$PROJECT_NAME", self.project_name)
        # write to ./Dockerfile
        with open("./Dockerfile", "w") as f:
            f.write(docker_data)

    def _update_settings(self):
        """Adds apps to INSTALLED_APPS in settings.py, adds required configuration"""
        with open(f"./{self.project_name}/settings.py", "r") as f:
            settings_data = f.read()
        # add additional configurations
        for service in self.service_settings:
            settings_data += "\n" + service + "\n"
        # add apps to INSTALLED_APPS
        installed_apps = settings_data.split("INSTALLED_APPS = [")[1].split("]")[0]
        app_lst = installed_apps.split(",")
        for app in self.apps:
            app_lst.append(f'"{app}.apps.{self._camel_casify(app)}Config"')
        if "scheduler" in self.services:
            app_lst.append('"django_rq"')
        app_lst = ", ".join(app_lst)
        settings_data = settings_data.replace(installed_apps, app_lst)
        with open(f"./{self.project_name}/settings.py", "w") as f:
            f.write(settings_data)

    def _update_urls(self):
        """Adds app urls to project urls.py"""
        with open(f"./{self.project_name}/urls.py", "r") as f:
            urls_data = f.read()
        # add apps to urlpatterns
        url_patterns = urls_data.split("urlpatterns = [")[1].split("]")[0]
        url_lst = url_patterns.split(",")
        for app in self.apps:
            url_lst.append(f'path("", include("{app}.urls"))')
        if "scheduler" in self.services:
            url_lst.append('path("django-rq/", include("django_rq.urls"))')
        url_lst = ", ".join(url_lst)
        urls_data = urls_data.replace(url_patterns, url_lst)
        with open(f"./{self.project_name}/urls.py", "w") as f:
            f.write(urls_data)

    def _camel_casify(self, s):
        s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
        return "".join([s[0].lower(), s[1:]])

    def _copy_project(self):
        # copy django project root folder
        shutil.copytree("./assets/django/dj_starter_pack", f"./{self.project_name}")
        if os.path.exists("./manage.py"):
            os.remove("./manage.py")
        shutil.copy("./assets/django/manage.py", "./manage.py")
        # rename files
        files_to_change = [
            "./manage.py",
            f"./{self.project_name}/settings.py",
            f"./{self.project_name}/wsgi.py",
            f"./{self.project_name}/asgi.py",
            f"./{self.project_name}/urls.py",
        ]
        for file in files_to_change:
            with open(file, "r") as f:
                filedata = f.read()
            filedata = filedata.replace("dj_starter_pack", self.project_name)
            with open(file, "w") as f:
                f.write(filedata)

    def _copy_apps(self):
        # copy the app_0 folder to the new project folder
        for app in self.apps:
            shutil.copytree("./assets/django/app_0", f"./{app}")
            # project_name replacement rename files
            with open(f"./{app}/apps.py", "r") as f:
                filedata = f.read()
            filedata = filedata.replace("dj_starter_pack", self.project_name)
            filedata.replace("App0Config", f"{self._camel_casify(app)}Config")
            with open(f"./{app}/apps.py", "w") as f:
                f.write(filedata)

    def _env(self):
        """Creates .env file with required variables"""
        with open("./.env", "w") as f:
            f.write("DJANGO_SECRET_KEY=" + secrets.token_urlsafe())
            f.write("DEBUG=True")
            f.write("DB_NAME=")
            f.write("POSTGRES_USER=")
            f.write("POSTGRES_PASSWORD=")
            if "email" in self.service_settings:
                f.write("EMAIL_HOST_USER=")
                f.write("EMAIL_HOST_PASSWORD=")
            if "redis" in self.services:
                f.write("REDIS_PASSWORD=")

    def _get_folder_structure(self):
        """
        This function returns the folder structure of the project in ascii
        """
        folder_struct = ""
        path = os.getcwd()
        for root, dirs, files in os.walk(path):
            # if .git continue
            if ".git" in root:
                continue
            level = root.replace(path, "").count(os.sep)
            indent = " " * 4 * (level)
            folder_struct += "{}{}/".format(indent, os.path.basename(root))
            subindent = " " * 4 * (level + 1)
            for f in files:
                folder_struct += "{}{}".format(subindent, f)
        return folder_struct

    def _readme(self):
        """Creates a README.md file with the project name and folder structure"""
        project_desc = input("One sentence to describer this project: ")
        with open("../assets/extras/README.md", "r") as f:
            readme_data = f.read()
        readme_data = readme_data.replace(
            "dj_starter_pack_folder_structure", self._get_folder_structure()
        )
        readme_data = readme_data.replace("dj_starter_pack", self.project_name)
        readme_data = readme_data.replace("dj_starter_pack_one_liner", project_desc)

        with open("./README.md", "w") as f:
            f.write(readme_data)

    def _requirements(self):
        """Creates a requirements.txt file with the project name and folder structure"""
        with open("./assets/requirements/requirements.main.txt", "r") as f:
            requirements_data = f.read()
        if "redis" in self.services:
            with open("./assets/requirements/requirements.redis.txt", "r") as f:
                requirements_data += f.read()
            if "scheduler" in self.services:
                with open("./assets/requirements/requirements.scheduler.txt", "r") as f:
                    requirements_data += f.read()

        with open("./requirements.txt", "w") as f:
            f.write(requirements_data)

    def _makefile(self):
        """Adds a Makefile with the project name and folder structure"""
        # move the makefile from assets to the project root
        shutil.copy("./assets/extras/Makefile", "./Makefile")

    def _pipeline(self):
        """Adds the Github Actions pipeline from ./assets/.github folder and replaces with the project name"""
        # add the .github folder
        shutil.copytree("./assets/.github", "./.github")
        # replace the project name in the pipeline
        with open("./.github/workflows/send-code-change.yml", "r") as f:
            pipeline_data = f.read()
        pipeline_data = pipeline_data.replace("$PROJECT_NAME", self.project_name)
        with open("./.github/workflows/send-code-change.yml", "w") as f:
            f.write(pipeline_data)

    def projectify(self):
        """Use the set configuration to create and manipulate the files for the project template"""
        self._copy_project()
        self._copy_apps()
        aggregate(self.services, self.project_name)
        self._update_settings()
        self._nginx()
        self._docker()
        self._env()
        self._requirements()
        self._makefile()
        self._pipeline()

    def destroy(self):
        """Deletes all of the files used to"""
        self._readme()
        shutil.rmtree("./assets")
        shutil.rmtree("./utils")
        im_done_done = input("Are you sure you are done? Remove the .git folder? (y/n)")
        if im_done_done == "y":
            shutil.rmtree("README.md")
            shutil.rmtree(".git")
            print("TODO:")
            print("Change the name of the root folder.")
            print("Initalize git repository `git init`")
            print("Set up pre-commit hooks `pre-commit install`")
