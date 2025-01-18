import os
import shutil
from website_generation import recursive_copy_static, generate_pages_recursive, markdown_path, template_path

from_path = "./static"
to_path = "./public"

def main():
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
        print(f"Removed {to_path} folder")
    print(f"Copying static files from {from_path} to public directory {to_path}")
    recursive_copy_static(from_path, to_path)
    print(f"Generating page to {to_path} using markdown from {markdown_path} and template from {template_path}")
    generate_pages_recursive(markdown_path, template_path, to_path)

main()
