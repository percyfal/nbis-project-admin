import pkg_resources
from jinja2 import Environment
from jinja2 import FileSystemLoader


template_path = pkg_resources.resource_filename("nbis", "templates")
file_loader = FileSystemLoader(template_path)
env = Environment(loader=file_loader)
