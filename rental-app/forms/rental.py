#!/usr/bin/env python3
# Generates the rental application form
# Open Applicaiton, fill application, submit application
from tkinter import *
from tkcalendar import DateEntry
import data.datastorage as ds
from datetime import datetime

# Variable Declaration
window = Tk()
fields = (
    "Full Legal Name",
    "Date of Birth",
    "SSN",
    "Drivers License",
    "Home Phone",
    "Work Phone",
    "Email",
    "Apartment",
    "Rent",
    "Start Date",
    "Agent/Referred By",
)

# Button Functions

## Function to take data from GUI window and write to an excel file
def saveAndClose(ent):
    ds.saveValues(ent)
    window.destroy()


## Create the calendar entry for Date of Birth
def createTkCalendar(window, entries, field, old_ent):
    old_ent.pack_forget()
    sel = StringVar()
    lab = Label(window)
    cal = DateEntry(window)
    if field == "Date of Birth":
        cal = DateEntry(
            window, selectmode="day", textvariable=sel, date_pattern="mm/dd/y"
        )
    else:
        cal = DateEntry(
            window,
            selectmode="day",
            textvariable=sel,
            mindate=datetime.now(),
            date_pattern="mm/dd/y",
        )
    lab.pack(side=RIGHT, expand=YES, fill=X)
    cal.pack(side=RIGHT, expand=YES, fill=X)

    # This sub function updates the label for the dates
    def my_upd(*args):
        lab.config(text=sel.get())

    sel.trace("w", my_upd)
    entries[field] = cal


def makeform(window, fields):
    entries = {}
    for field in fields:
        row = Frame(window)
        lab = Label(row, width=22, text=field + ": ", anchor="w")
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
        if field == "Date of Birth":
            createTkCalendar(row, entries, field, ent)
        if field == "Start Date":
            createTkCalendar(row, entries, field, ent)
    return entries


def createRentalForm():
    # Create Window
    # window.geometry("500x500")
    window.geometry("")
    window.title("Rental Application Form")

    ents = makeform(window, fields)

    # create a Submit Button and place into the root window
    submit = Button(
        window,
        text="Submit",
        fg="White",
        bg="Red",
        command=(lambda e=ents: saveAndClose(e)),
    ).pack(side=LEFT, padx=5, pady=5)

    # Start form
    window.mainloop()
