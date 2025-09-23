"""

i currently have a dataset of 120 gb
- remove unnecessary files (images, videos, maybe excel?)
- check dataset size, if too large: remove each folder with x% probability, define seed
- if still too large: can remove files larger than x mb

after delete_extension there is 45 gb of data
and in clouddevels there is roughly 10-12 gb size
so randomly delete some folders
--> with 75% probability, there is at the end 8 gb data left

"""

import os
import subprocess
import random

curr_user = os.environ.get('USERNAME')
mydir = "C:/Users/" + curr_user + "/Desktop/"
##mydir = "C:\\"
os.chdir(mydir)

foldername = "3 Leistungserbringung"
errors = set()

def delete_extension(full_path):
    extensions = [".docx", ".txt", ".pdf", ".pptx", ".eml"]
    file_extension = os.path.splitext(file)

    if file_extension[1] not in extensions:
        # os.remove is broken due to windows filepath char limit
        result = subprocess.run(['del', '/f', '/q', full_path],
                                shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Deleted: {file}")
        else:
            errors.add(f"Failed to delete {full_path}: {result.stderr}")

def delete_folder(folder_path):
    random.seed(1)
    prob = 0.75 # deletion probability for dossiers
    if random.random() < prob:
        result = subprocess.run(['rmdir', '/s', '/q', folder_path], 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Force deleted folder: {folder_path}")
        else:
            errors.add(f"Failed to delete {full_path}: {result.stderr}")

for dirpath, dirnames, filenames in os.walk(foldername):
##    print(dirpath) ## current directory (relative path to beginning of walk)
##    print(dirnames) ## list of folders in current directory
##    print(filenames) ##list of files in current directory
    for file in filenames:

####  delete extension files
##    for file in filenames:
##        full_path = os.path.join(dirpath, file)
##        delete_extension(full_path)

####  delete folders
##    if dirnames == []:
##        delete_folder(dirpath)
        

