import json

from common import make_resource

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
