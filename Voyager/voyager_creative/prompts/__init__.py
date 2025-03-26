import pkg_resources
import voyager_creative.utils as U


def load_prompt(prompt):
    package_path = pkg_resources.resource_filename("voyager_creative", "")
    return U.load_text(f"{package_path}/prompts/{prompt}.txt")
