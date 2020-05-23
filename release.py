import os
from zipfile import ZipFile, ZIP_BZIP2
import json
from os.path import basename
from fnmatch import fnmatch

# Read version from info.json
with open('info.json', 'r') as info_file:
    info = info_file.read()
info = json.loads(info)
version = info['version']

print(f"version {version}")

# Create a zip
root_folder_name = f'factorio-world_{version}'
excludes = [
    'MapGenerator',
    '.vscode',
    '.git',
    '.gitignore',
    'Screenshots',
    '*.zip',
    '*.py',
    '*.txt',
]
with ZipFile(f'{root_folder_name}.zip', 'w', ZIP_BZIP2) as zipObj:
    # Iterate over all the files in directory
    for folderPath, subfolders, filenames in os.walk('.'):
        folders = os.path.normpath(folderPath).split(os.sep)
        if any([any([fnmatch(f, e) for f in folders]) for e in excludes]): continue

        for filename in filenames:
            if any([fnmatch(filename, e) for e in excludes]): continue

            file_path = os.path.join(folderPath, filename)
            in_zip_path = os.path.join(root_folder_name, folderPath, filename)
            print("Adding file:", file_path, "to zip at", in_zip_path)
            
            # Add file to zip
            zipObj.write(file_path, in_zip_path)
