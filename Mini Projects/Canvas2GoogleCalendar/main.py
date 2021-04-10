import requests
from tkinter import *
from datetime import date
from convert_outdated import change_sum


class Calendar:
    def __init__(self, c):
        self.c = c


class Name:
    def __init__(self):
        self.root = Tk()
        self.url = open("cal_address.txt", "r").readlines()[0].replace("\n", "")  # <-- paste your url here!
        self.txt = requests.get(self.url, stream=True)
        self.calendar = re.finditer(r"(BEGIN:VEVENT)(.*?)\s(.*?)\s(^END:VEVENT)", self.txt.text, re.DOTALL | re.M)
        self.filters = ["due", "lab"]

        self.pressed = False
        self.d, self.dd, self.frames = dict(), dict(), []

    def first_loop(self):
        calendar = []
        for n in self.calendar:
            n = n.group(0)
            dtstart = re.search(r"(?<=(:)).*$", re.search(r"DTSTART(.*)", n).group(0)).group(0).split("T")[0]
            dtend = re.search(r"(?<=(:)).*$", re.search(r"DTEND(.*)", n).group(0)).group(0).split("T")[0]
            yy, mm, nn = dtend[:4], dtend[4:6], dtend[6:]

            ### Except
            # print("\n"* 50)
            # dtend = dtstart = None
            # yy, mm, nn = 1000, 1, 1
            if date(int(yy), int(mm), int(nn)) >= date.today():

                line = re.search(r"\bSUMMARY\b(.*?)\s(.*?)\s(URL:)", n).group(0)[:-4]
                line = re.sub(r"\r|\n|\\|,", "", line)

                m = [k for k in re.finditer(r"[A-Z]{3,5}\s?([0-9]{1,3}[A-Z]?)", line)][-1].group(0).upper()
                m = re.sub(r"([A-Z]{1,6}?(?=\d))", r'\1 ', m)

                classifier = None
                if "lab" in line.lower():
                    classifier = "lab"
                if "discussion" in line.lower():
                    classifier = "discussion"

                if not any(x in m.lower() for x in self.filters):
                    if m not in self.d:
                        self.d[m] = []
                    elif classifier and classifier not in self.d[m]:
                        self.d[m].append(classifier)
                if "assignment" in re.search(r"\bUID:(.*)", n).group(0):
                    classifier = "assignment"
                if not classifier:
                    classifier = "lecture"

                if "office h" not in line.lower() and "oh" not in line.lower():
                    calendar.append(
                        {
                            "text": n,
                            "course_name": m,
                            "summary": line,
                            "classifier": classifier,
                            "start": dtstart,
                            "end": dtend,
                        }
                    )

        return calendar

    def second_loop(self):
        cal = "BEGIN:VCALENDAR\nVERSION:2.0\n\n"
        for n in self.calendar:
            # if "mentor" in n["summary"].lower():
            #     print(n["text"])
            if n["course_name"] in self.dd:
                if n["classifier"] in self.dd[n["course_name"]]:
                    section = self.dd[n["course_name"]][n["classifier"]]
                    if not section or section not in n["summary"]:
                        continue

                line, txt = change_sum(n["text"])
                # print(n["classifier"], re.search(r'\bSUMMARY\b(.*)', txt).group(0))
                cal += txt + "\n\n"
        with open('optimized_calendar.ics', 'w') as f:
            cal += "\nEND:VCALENDAR"
            cal = re.sub(r"\s]\n", "", cal)
            f.write(cal)

    def quit_(self, press=False):
        for i in self.dd:
            for j in self.dd[i]:
                if press:
                    self.dd[i][j] = self.dd[i][j].get().upper()
                else:
                    self.dd[i][j] = ""
        self.pressed = True
        self.root.quit()

    def tk_get_session(self):
        self.calendar = self.first_loop()

        self.root.title('Get session info')
        self.root.geometry("600x400")
        Label(self.root, text="Please provide your session number for following courses:",
              font=("Arial", 11, "bold"), foreground="#297373").grid(row=0, column=0, sticky="w")
        Label(self.root, text="(Leave it blank if you DO NOT wish to include this section)",
              font=("Arial", 10), foreground="#297373").grid(row=1, column=0, sticky="w")

        for i, items in enumerate(self.d):
            self.dd[items] = dict()
            self.frames.append(Frame(self.root, height=20, width=500))

            if self.d[items]:
                Label(self.frames[i], text=f"{items}:", foreground="#FF8552",
                      font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w")

            for j, item in enumerate(self.d[items]):
                Label(self.frames[i], text=f"{item}:", foreground="#36453B", font=("Arial", 10)
                      ).grid(row=j + 1, column=0, sticky="w")
                self.dd[items][item] = Entry(self.frames[i], width=100)
                self.dd[items][item].grid(row=j + 1, column=1, sticky="w")

            self.frames[i].grid(row=i + 2, column=0, sticky="w")

        end_frame = Frame(self.root)
        Button(end_frame, text="Save", pady=7, padx=18, command=(lambda x=True: self.quit_(press=x)), fg="#E6E6E6",
               bg="#39393A", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="ew", pady=40, padx=0)
        end_frame.grid(column=0, sticky="nsew")
        mainloop()
        if not self.pressed:
            self.quit_()

        self.second_loop()


c = Name()
c.tk_get_session()
