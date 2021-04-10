import re
import sys
import requests
import subprocess
from colors import Color
from datetime import date

co = Color()
d = {}
alarm5m = """
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:This is an event reminder
TRIGGER:-P0DT0H5M0S
END:VALARM"""
alarm1d = """
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:This is an event reminder
TRIGGER:-P1DT0H0M0S
END:VALARM"""
# Notify 5 minutes before event starts


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

    # line = re.sub(rf"\b{name}\b(\s-\s)?", "", line)
    line = re.sub(rf"([0-9]{1, 5}(\s-\s)|\b{name}\b(\s-\s)?)", "", line)
    name = re.sub(r"([A-Z]{1,6}?(?=\d))", r'\1 ', name)
    if name not in d:
        d[name] = co.rand_c()
    line = re.sub(r"\\||,|(\[|\()(.*)", "", line)
    line = re.sub(r"\s\s", r" ", line)
    if name is not None:
        line = re.sub(line, rf"{name} {line}", line)
    line = "SUMMARY:" + line

    uid = re.search(r'\bUID:\b(.*)', evt).group(0)
    if "exam" in line.lower() or "quiz" in line.lower() or "midterm" in line.lower() or "mid term" in line.lower() \
            or "final" in line.lower():
        line = re.sub(r"\bSUMMARY:\b([A-Z]{3,5}\s?([0-9]{1,3}[A-Z]?))", r"SUMMARY:\1 (Q)", line)
        evt = re.sub(r'\bSUMMARY\b(.*)', rf"COLOR:{d[name]}{alarm5m}\n{line}", evt)
    elif "assignment" in uid:
        line = re.sub(r"\bSUMMARY:\b([A-Z]{3,5}\s?([0-9]{1,3}[A-Z]?))", r"SUMMARY:\1 (A)", line)
        evt = re.sub(r'\bSUMMARY\b(.*)', rf"COLOR:{d[name]}{alarm1d}\n{line}", evt)
    elif "lab" in line.lower():
        line = re.sub(line, rf"SUMMARY:{name} Lab", line)
        evt = re.sub(r'\bSUMMARY\b(.*)', rf"COLOR:{d[name]}{alarm5m}\n{line}", evt)
    elif "discussion" in line.lower():
        line = re.sub(line, rf"SUMMARY:{name} Discussion", line)
        evt = re.sub(r'\bSUMMARY\b(.*)', rf"COLOR:{d[name]}{alarm5m}\n{line}", evt)
    else:
        line = re.sub(line, rf"SUMMARY:{name} Lecture", line)
        evt = re.sub(r'\bSUMMARY\b(.*)', rf"COLOR:{d[name]}{alarm5m}\n{line}", evt)

    evt = re.sub(r"\r", "", evt)
    evt = re.sub(r"\bCLASS:PUBLIC\b", "CLASS:PRIVATE", evt)


    return line, evt


def main():
    try:
        from ics import Calendar, Event
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    finally:
        from ics import Calendar, Event
    # install required packages

    try:
        url = open("cal_address.txt", "r").readlines()[0].replace("\n", "")
    except FileNotFoundError:
        print("Please create \"cal_address.txt\" and copy your ics url into it")
        sys.exit(1)

    txt = requests.get(url).text
    txt = re.sub(r"\bCLASS:PUBLIC\b", "CLASS:PRIVATE", txt)  # change class
    cal = Calendar(txt)
    new_cal = Calendar()

    for i, ev in enumerate(list(cal.timeline)):
        sum_name = str(ev.name)
        dt = str(ev.end).split("T")[0]
        yy, mm, nn = dt.split("-")

        if name_filter(sum_name, lab="04") and date(int(yy), int(mm), int(nn)) >= date.today():
            name, ev = change_sum(ev)

            # print(name, "\n")
            new_cal.events.add(ev)

    with open('new_cal.ics', 'w') as f:
        f.write(str(new_cal))


if "__main__" == "__name__":
    main()
