# this file aggregates multiple docker-compose files into a single one

import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def aggregate(services=["postgres", "nginx", "django"]):
    """Takes a list of services and uses existing compose files to aggregate into single file"""
    yml = {
        "volumes": {},
        "services": {},
    }
    docker_compose_paths = [
        f"../assets/compose/docker-compose.{service}.yaml" for service in services
    ]
    for path in docker_compose_paths:
        with open(path, "r") as ymlfile:
            file_yml = yaml.load(ymlfile, Loader=yaml.FullLoader)
            yml["services"].update(file_yml["services"])
            yml["volumes"].update(file_yml.get("volumes", {}))
    yml["version"] = 3
    with open("../docker-compose.yaml", "w") as yml_compiled:
        yaml.dump(yml, yml_compiled, default_flow_style=False)


if __name__ == "__main__":
    aggregate()
