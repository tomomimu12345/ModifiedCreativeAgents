import pkg_resources
import os
import voyager_creative.utils as U


def load_control_primitives(use_command, primitive_names=None):
    package_path = pkg_resources.resource_filename("voyager_creative", "")
    if primitive_names is None:
        primitive_names = [
            primitives[:-3]
            for primitives in os.listdir(f"{package_path}/control_primitives")
            if primitives.endswith(".js")
        ]
    if use_command:
        primitive_names.remove("placeItem")
    else:
        primitive_names.remove("placeItem_command")
    print(primitive_names)
    
    primitives = [
        U.load_text(f"{package_path}/control_primitives/{primitive_name}.js")
        for primitive_name in primitive_names
    ]
    return primitives
