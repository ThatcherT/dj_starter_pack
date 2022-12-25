import os

def rename_project():
    while True:
        project_name = input("1/8. Project Name: ")
        if project_name:
            # rename project_dir
            os.rename("./dj_starter_pack", f"./{project_name}")
            # rename files
            files_to_change = [
                "./manage.py",
                "./dj_starter_pack/settings.py",
                "./dj_starter_pack/wsgi.py",
                "./dj_starter_pack/asgi.py",
                "./dj_starter_pack/urls.py",
            ]
            for file in files_to_change:
                with open(file, "r") as f:
                    filedata = f.read()
                filedata = filedata.replace("dj_starter_pack", project_name)
                with open(file, "w") as f:
                    f.write(filedata)
            break