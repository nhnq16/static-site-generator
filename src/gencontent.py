import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    for entry in os.scandir(dir_path_content):
        if entry.is_file() and entry.name.endswith('.md'):
            relative_path = os.path.relpath(entry.path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + '.html')
            generate_page(entry.path, template_path, dest_path)
        elif entry.is_dir():
            sub_dest_dir = os.path.join(dest_dir_path, entry.name)
            generate_pages_recursive(entry.path, template_path, sub_dest_dir)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")
