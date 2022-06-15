from jinja2 import Environment
from jinja2 import FileSystemLoader
import pkg_resources


template_path = pkg_resources.resource_filename("nbis", "templates")
file_loader = FileSystemLoader(template_path)
env = Environment(loader=file_loader)
