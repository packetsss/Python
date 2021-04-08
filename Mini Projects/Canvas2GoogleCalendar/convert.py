import re
import requests
from colors import Color
from datetime import date
from ics import Calendar, Event

url = open("cal_address.txt", "r").readlines()[0]

txt = requests.get(url).text
txt = re.sub(r"\bCLASS:PUBLIC\b", "CLASS:PRIVATE", txt)  # change class

cal = Calendar(txt)
new_cal = Calendar()

co = Color()
d = {}
alarm = """
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:This is an event reminder
TRIGGER:-P0DT0H5M0S
END:VALARM"""

def name_filter(string, lab=None):
    string = string.lower()
    if "office hour" in string or "oh" in string:
        return False
    if "lab" in string and (not lab or lab not in string):
        return False
    if ("di" in string or "discussion section" in string) and "reading" not in string:
        return False
    if "optional" in string:
        print("\n\n\n1231231231321\n\n\n")
    return True


def change_sum(evt):
    evt = str(evt)
    ln = re.search(r"\bSUMMARY\b(.*)", evt)
    line = re.sub(r"\bSUMMARY:\b", "", ln.group(0))
    if "due" not in line.lower():
        name = re.search(r"[A-Z]{3,5}\s?([0-9]{1,3}[A-Z]?)", line).group(0)
    else:
        ss = line.lower().replace("due", "")
        name = [m for m in re.finditer(r"[a-z]{3,5}\s?([0-9]{1,3}[a-z]?)", ss)][-1].group(0).upper()

    line = re.sub(rf"\b{name}\b(\s-\s)?", "", line)
    line = re.sub(r"[0-9]{1,5}(\s-\s)", "", line)
    name = re.sub(r"([A-Z]{1,6}?(?=\d))", r'\1 ', name)
    if name not in d:
        d[name] = co.rand_c()
    line = re.sub(r"(\[|\()(.*)", "", line)
    line = re.sub(r"\\", "", line)
    if name is not None:
        line = re.sub(line, rf"{name} {line}", line)
    line = re.sub(r"\s\s", r" ", line)
    line = "SUMMARY:" + line

    uid = re.search(r'\bUID:\b(.*)', evt).group(0)
    if "exam" in line.lower() or "quiz" in line.lower() or "midterm" in line.lower() or "mid term" in line.lower() \
            or "final" in line.lower():
        line = re.sub(r"\bSUMMARY:\b([A-Z]{3,5}\s?([0-9]{1,3}[A-Z]?))", r"SUMMARY:\1 (Q)", line)
    elif "assignment" in uid:
        line = re.sub(r"\bSUMMARY:\b([A-Z]{3,5}\s?([0-9]{1,3}[A-Z]?))", r"SUMMARY:\1 (A)", line)
    elif "lab" in line.lower():
        line = re.sub(r"\bSUMMARY:\b([A-Z]{3,5}\s?([0-9]{1,3}[A-Z]?))", r"SUMMARY:\1 (L)", line)
    else:
        line = re.sub(line, rf"SUMMARY:{name} Lecture", line)

    evt = re.sub(r'\bSUMMARY\b(.*)', rf"{line}\nCOLOR:{d[name]}{alarm}", evt)
    evt = re.sub(r"(\r|\.|,)", "", evt)

    return line, evt


for i, ev in enumerate(list(cal.timeline)):
    sum_name = str(ev.name)
    dt = str(ev.end).split("T")[0]
    yy, mm, nn = dt.split("-")

    if name_filter(sum_name, lab="04") and date(int(yy), int(mm), int(nn)) >= date.today():
        name, ev = change_sum(ev)

        # print(name, "\n")
        new_cal.events.add(ev)

print(d)

with open('new_cal.ics', 'w') as f:
    f.write(str(new_cal))


