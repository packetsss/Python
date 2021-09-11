# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

class student:

    def __init__(self, name, major, gpa, probation):
        self.name = name
        self.major = major
        self.gpa = gpa
        self.probation = probation

    def on_honor_roll(self):
        if self.gpa >= 3.5:
            return True
        else:
            return False
