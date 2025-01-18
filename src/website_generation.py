import shutil
import os
from block_markdown import markdown_to_html_node, extract_title
markdown_path = "./content/index.md"
template_path = "./template.html"
dest_path = "./public/index.html"

# Former implementation allowed to delete only the files that were present in both folders
def recursive_copy_static(src, dst):
#    if not os.path.exists(src):
        #raise Exception(f"{src} src directory doesn't exist")
    #if not os.path.exists(dst):
        #raise Exception(f"{dst} dst directory doesn't exist")
    #src_dir_list = os.listdir(src)
    #for dir in src_dir_list:
        #join_dirs = os.path.join(dst, dir)
        #if os.path.isfile(join_dirs):
            #if os.path.exists(join_dirs):
                #os.remove(join_dirs)
                #print(f"Erased {join_dirs} file")
        #else:
            #if os.path.exists(join_dirs):
                #shutil.rmtree(join_dirs)
                #print(f"Removed {join_dirs} dir")
    if not os.path.exists(dst):
        os.mkdir(dst)
    src_dir_list = os.listdir(src)  
    for dir in src_dir_list:
        join_src_dirs = os.path.join(src, dir)
        join_dst_dirs = os.path.join(dst, dir)
        if os.path.isfile(join_src_dirs):
            shutil.copy(join_src_dirs, dst)
        else:
            #os.mkdir(join_dst_dirs)
            #print(f"Created {join_dst_dirs} folder")
            recursive_copy_static(join_src_dirs, join_dst_dirs)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    with open(from_path, mode = "r") as f:
        markdown = f.read()
    with open(template_path, mode = "rt") as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    markdown_title = extract_title(markdown)
    updated_template = template.replace("{{ Title }}", markdown_title) .replace("{{ Content }}", html_string)
    dest_dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_name):
        os.makedirs(dest_dir_name) 
    with open(dest_path, "w") as f:
        f.write(updated_template)
