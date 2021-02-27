class Chef:

    def make_chicken(self):
        print("The chef makes chicken")

    def make_oliver(self):
        print("The chef can make oliver")

    def make_special(self):
        print("The chef can make steak")


myChef = Chef()
myChef.make_chicken()
myChef.make_special()


class ChineseChef(Chef):

    def make_fried_rice(self):
        print("The chef can make fried rice")
    def make_special(self):
        print("The chef can make Goofy chicken")


ChineseChef().make_fried_rice()
ChineseChef().make_special()
