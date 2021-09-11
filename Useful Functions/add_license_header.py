# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import os
import re
import pdb
from tkinter import Tk
from itertools import islice
from tkinter import filedialog


def select_target_files(
    repo_path,
    file_exclude_pattern=True,
    dir_exclude_pattern=None,
    exclude_hidden_directories=True,
):
    full_paths = []

    for root, dirs, files in os.walk(repo_path):
        if exclude_hidden_directories:
            dirs[:] = [d for d in dirs if not d[0] == "."]
        if dir_exclude_pattern:
            dirs[:] = [d for d in dirs if not re.match(dir_exclude_pattern, d)]
        if file_exclude_pattern:
            files[:] = [f for f in files if ".py" == f[-3:]]
        full_paths += [os.path.join(root, f) for f in files]

    return full_paths


def format_license(string, style="# "):
    N = string.count("\n")
    if style == "# ":
        return style + string.replace("\n", "\n" + style, N - 1)
    raise Exception("new style definition needed for " + style)


def starts_with(file, string):
    N = string.count("\n")
    assert N > 0
    with open(file, encoding="utf-8") as f:
        head = list(islice(f, N))
    return head == string


def prepend(license_file, files, styles=None, extra_blank_lines=1):
    # Load license text
    with open(license_file) as lf:
        license_str = lf.read()
    if not license_str[-1:] == "\n":
        license_str += "\n"
    # Format the license
    # TODO: move some/all of this formatting inside the file loop after making it depend on file type
    ready_license_str = format_license(license_str)
    for i, file in enumerate(files):
        if starts_with(file, ready_license_str):
            continue
        with open(file, encoding="utf-8") as f:
            try:
                file_str = f.read()
            except:
                raise Exception("failed to read file " + file)
        if "#" in file_str[:2]:
            continue
        with open(file, "w", encoding="utf-8") as f:
            f.write(ready_license_str + "".join(["\n"] * extra_blank_lines) + file_str)
        print(f"The {i}th file finished processing: " + str(file.split('\\')[-1].split('/')[-1]))


if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    folder_selected = filedialog.askdirectory()
    files = select_target_files(folder_selected)

    license_file = filedialog.askopenfilename()
    prepend(license_file, files)
