# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import re
import os
import sys
from tkinter import Tk
from tkinter import filedialog


def is_camel(word):
    if "." in word:
        return None
    bol = re.search('\w([a-z][A-Z])', word)
    
    return bol


def convert(word):
    if re.search('\S=\S', word) is not None:
        return word
    word = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    word = re.sub('([a-z0-9])([A-Z])', r'\1_\2', word).lower()
    return word


root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

for root, dirs, files in os.walk(folder_selected):
    for name in files:

        FILE_NAME = os.path.join(root, name)
        if FILE_NAME[-3:] != ".py":
            continue
        print(f"{name} converted")
        OLD_FILE = open(FILE_NAME).read()
        NEW_FILE = open(FILE_NAME, 'w')
        for w in OLD_FILE.split():
            if is_camel(w) != None:
                OLD_FILE = OLD_FILE.replace(w, convert(w))
        NEW_FILE.write(OLD_FILE)

print("Convention changed to snake case successfully!")
