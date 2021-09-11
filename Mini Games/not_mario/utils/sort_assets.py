# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import os
import re
import shutil

rootdir = None

# Uncomment the line below with CAUTION
# rootdir = r'C:\Users\pyjpa\Desktop\Programming\Python\Mini Games\fake_mario\assets'

folder_name = "Walk"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)

        if re.search(folder_name, path):
            # print(file)

            source = re.sub(r"\\(?:.(?!\\))+$", r"\\", path)
            destination = source + f"{folder_name}\\"
    
            if not os.path.exists(destination):
                os.makedirs(destination)

            shutil.move(os.path.join(source, file), os.path.join(destination, file))