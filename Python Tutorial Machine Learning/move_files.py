import os
import re
import shutil

# Uncomment the line below with CAUTION
# rootdir = 'C:\\Users\\pyjpa\\Desktop\\Python Tutorial Machine Learning'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)

        if re.search(r"(\.ipynb)|(\.py)", path):
            # print(path)
            source = re.sub(r"\\(?:.(?!\\))+$", r"\\", path)
            destination = re.search(r"(.*)Part (.*?)\\", path)
            if destination is not None:
                destination = destination.group(0)
                # print(destination)

                file_names = os.listdir(source)
    
                for file_name in file_names:
                    shutil.move(os.path.join(source, file_name), os.path.join(destination, file_name))
                
                file_names = os.listdir(destination)
                for f in file_names:
                    if os.path.isdir(os.path.join(destination, f)):
                        shutil.rmtree(os.path.join(destination, f))