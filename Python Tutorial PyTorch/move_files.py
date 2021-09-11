# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import os
import re
import shutil

# Uncomment the line below with CAUTION!!
# rootdir = 'C:\\Users\\pyjpa\\Desktop\\Python Tutorial PyTorch\\src'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)

        if re.search(r"(\.ipynb)|(\.py)", path):
            if not re.search(r"(\\notebook_source_)", path):

                source = re.sub(r"\\(?:.(?!\\))+$", r"\\", path)

                destination = "C:\\Users\\pyjpa\\Desktop\\Python Tutorial PyTorch"

                file_name = [re.search(f, path,) for f in os.listdir(source) if re.search(f, path) is not None][0].group(0)
                print(source)
                shutil.move(os.path.join(source, file_name), os.path.join(destination, file_name))
            else:
                source = re.sub(r"\\(?:.(?!\\))+$", r"\\", path)[:-1]
                source = re.search(r"\\(?:.(?!\\))+$", source).group(0)
                file_name = source[1:] + ".ipynb"
                
                if file_name:
                    destination = "C:\\Users\\pyjpa\\Desktop\\Python Tutorial PyTorch"
                    s = re.sub(r"\\(?:.(?!\\))+$", r"\\", path)
                    f = [re.search(f, path) for f in os.listdir(s) if re.search(f, path) is not None][0].group(0)
                    print(f)
                    os.rename(os.path.join(s, f), os.path.join(s, file_name))
                    shutil.move(os.path.join(s, file_name), os.path.join(destination, file_name))

