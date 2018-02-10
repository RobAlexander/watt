from jinja2 import Environment, FileSystemLoader

import os
import json

def jinja2_tex_escape(content):
    return str(content).replace("%", "\\%")

jinja2_custom_filters = {
    'tex_escape': jinja2_tex_escape
}

def make_resource(template, file_path, **args):
    jinja_env = Environment(loader=FileSystemLoader('templates/'))
    jinja_env.filters.update(jinja2_custom_filters)
    template = jinja_env.get_template(template)
    resource = template.render(**args)
    with open(file_path, 'w') as f:
        f.write(resource)

def pages_table(pages_desc_file, pages_tex_file="pages.tex"):
    page_descriptions = {}
    with open(pages_desc_file) as f:
        page_descriptions = json.load(f)
    for page in page_descriptions.keys():
        if page_descriptions[page][-1] == '\n':
            page_descriptions[page] = page_descriptions[page][:-1]
    make_resource("pages.tex.jinja2", pages_tex_file,
                  pages=sorted(page_descriptions.keys()), page_descriptions=page_descriptions
                 )


if __name__ == '__main__':
    pages_table('pages.json')
