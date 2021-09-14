# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import re
import os
import sys
from tkinter import Tk
from tkinter import filedialog


def is_camel(word):
    #if "." in word or re.search('\S=\S', word) is not None or "Error" in word:
    #    return None
    bol = re.search('\w([a-z][A-Z])', word)
    return bol


def convert(word):
    word = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    word = re.sub('([a-z0-9])([A-Z])', r'\1_\2', word).lower()
    return word


root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

for root, dirs, files in os.walk(folder_selected):
    for name in files:

        file_name = os.path.join(root, name)
        if file_name[-3:] != ".py":
            continue
        
        old_file = open(file_name).read()
        new_file = open(file_name, 'w')
        ct = 0
        for w in old_file.split():
            if is_camel(w) != None:
                ct += 1
                old_file = old_file.replace(w, convert(w))
        
        new_file.write(old_file)
        print(f"{name} converted with {ct} convertions!")

print("Convention changed to snake case successfully!")
