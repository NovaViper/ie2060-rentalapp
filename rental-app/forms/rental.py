#!/usr/bin/env python3
# Generates the rental application form
# Open Applicaiton, fill application, submit application
from tkinter import *
from tkcalendar import DateEntry
import data.datastorage as ds

# Variable Declaration
window = Tk()
fields = (
    "First Name",
    "Middle Name",
    "Last Name",
    "SSN",
    "Date of Birth",
    "Drivers License",
    "Home Phone",
    "Work Phone",
    "Email",
    "Apartment",
    "Rent",
    "Start Date",
    "Agent/Referred By",
    "",
)
# Button Functions


# Function to take data from GUI window and write to an excel file
def saveAndClose(ent):
    ds.saveValues(ent)
    window.destroy()


# Create the calendar entry for Date of Birth
def createTkCalendar(window, entries, field, old_ent):
    old_ent.pack_forget()
    sel = StringVar()
    lab = Label(window)
    cal = DateEntry(window, selectmode="day", textvariable=sel)
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
        if field == "Move-In Date":
            createTkCalendar(row, entries, field, ent)
    return entries


def createRentalForm():
    # Create Window
    window.geometry("500x500")
    window.title("Rental Application Form")

    ents = makeform(window, fields)

    # Create Elements
    # firstName = Label(window, text="First Name").grid(row=0, column=0)
    # middleName = Label(window, text="Middle Name").grid(row=1, column=0)
    # lastName = Label(window, text="Last Name").grid(row=2, column=0)
    # ssn = Label(window, text="S.S.# Name").grid(row=3, column=0)
    # dob = Label(window, text="Date of Birth").grid(row=4, column=0)
    # moveindate = Label(window, text="When would you like to move in?").grid(row=5, column=0)
    # driverlicense = Label(window, text="Drivers License").grid(row=6, column=0)

    # Labels
    # firstNameBox = Entry(window).grid(row=0, column=1)

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
