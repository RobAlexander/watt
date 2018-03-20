from jinja2 import Environment, FileSystemLoader

import os

nan = float('nan')

def jinja2_tex_escape(content):
    return str(content).replace("%", "\\%")

jinja2_custom_filters = {
    'tex_escape': jinja2_tex_escape
}

def make_resource(template, file_path, **args):
    jinja_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/')))
    jinja_env.filters.update(jinja2_custom_filters)
    template = jinja_env.get_template(template)
    resource = template.render(**args)
    with open(file_path, 'w') as f:
        f.write(resource)
