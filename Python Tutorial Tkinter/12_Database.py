# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from tkinter import *
import sqlite3
# database lib


root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")
#root.geometry("400x400")

# c.execute('''CREATE TABLE addresses(
#         first_name text,
#         last_name text,
#         address text,
#         city text,
#         state text,
#         zipcode integer
#         )''')
# create table


def submit():
    conn = sqlite3.connect("src\\address_book.db")
    # automatically create for me

    c = conn.cursor()
    # create cursor
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
              {
                  "f_name": f_name.get(),
                  "l_name": l_name.get(),
                  "address": address.get(),
                  "city": city.get(),
                  "state": state.get(),
                  "zipcode": zipcode.get()
              })

    conn.commit()
    # need to commit

    conn.close()
    # need to close
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


def delete():
    conn = sqlite3.connect("src\\address_book.db")

    c = conn.cursor()
    c.execute(f"DELETE from addresses WHERE oid = {delete_box.get()}")
    delete_box.delete(0, END)

    conn.commit()
    conn.close()

def query():
    conn = sqlite3.connect("src\\address_book.db")

    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()

    print_record = ""
    for record in records:
        print_record += str(record) + "\n"

    query_label = Label(root, text=print_record)
    query_label.grid(row=11, column=0, columnspan=2)

    conn.commit()
    conn.close()


f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20)
address = Entry(root, width=30)
address.grid(row=2, column=1, padx=20)
city = Entry(root, width=30)
city.grid(row=3, column=1, padx=20)
state = Entry(root, width=30)
state.grid(row=4, column=1, padx=20)
zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1, padx=20)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)
# create input

f_name_label = Label(root, text="First name")
f_name_label.grid(row=0, column=0)
l_name_label = Label(root, text="Last name")
l_name_label.grid(row=1, column=0)
address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)
city_label = Label(root, text="City")
city_label.grid(row=3, column=0)
state_label = Label(root, text="State")
state_label.grid(row=4, column=0)
zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

delete_box_label = Label(root, text="Delete ID")
delete_box_label.grid(row=9, column=0)
# create label

submit_btn = Button(root, text="Add to DB", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=110)

query_btn = Button(root, text="Show records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=101)

delete_btn = Button(root, text="Delete records", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=98)

mainloop()
