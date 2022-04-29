#!/usr/bin/env python3
# Generates the rental application form
# Open Applicaiton, fill application, submit application
from tkinter import *
from tkcalendar import DateEntry
import data.datastorage as db
from datetime import datetime

# Variable Declaration
window = Tk()
fields = (
    "Full Legal Name",
    "Date of Birth",
    "Home PN",
    "Work PN",
    "Email Address",
    "SSN",
    "Drivers License",
    "Property Address",  # 8
    "Proposed Rent",
    "Start of Rental",
    "Agent/Referred By",
    "Current Full Address",  # 12
    "Date In",
    "Date Out",
    "Current Rent",
    "Reason for Moving",
    "Landlord",
    "Landlord PN",
)  # 19

# Element Functions
## Function to take data from GUI window and write to an excel file
def saveAndClose(ent):
    db.saveValues(ent)
    window.destroy()


def createNumberOnly(window, field, reg, old_ent):
    old_ent.pack_forget()
    text = StringVar()  # the text in  your entry
    ent = Entry(window, textvariable=text)

    ent.config(textvariable=text, validate="key", validatecommand=(reg, "%S"))
    if field == "SSN" or field == "Drivers License":
        text.trace("w", lambda *args: db.character_limit(text, 9))
    elif field.find("PN"):
        text.trace("w", lambda *args: db.character_limit(text, 10))
    ent.pack(side=RIGHT, expand=YES, fill=X)

    return ent


## Create the calendar entry for Date of Birth
def createTkCalendar(window, field, old_ent):
    old_ent.pack_forget()
    sel = StringVar()
    lab = Label(window)
    cal = DateEntry(window)
    if not field == "Start of Rental":
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
    return cal


def createGenEntry(windows, field, loc):
    regLetters = window.register(db.verifyForLetters)
    regNum = window.register(db.verifyForNumbers)
    row = Frame(windows)
    lab = Label(row, text=field + ": ", anchor="w")
    ent = Entry(row)
    row.pack(side=loc, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)

    if (
        field == "Full Legal Name"
        or field == "Agent/Referred By"
        or field == "Landlord"
    ):
        ent.config(validate="key", validatecommand=(regLetters, "%S"))
    # if field.find("PN"):

    if (
        field == "SSN"
        or field == "Drivers License"
        or field == "Home PN"
        or field == "Work PN"
        or field == "Landlord PN"
    ):
        createNumberOnly(row, field, regNum, ent)
    if (
        field == "Date of Birth"
        or field == "Start of Rental"
        or field == "Date In"
        or field == "Date Out"
    ):
        createTkCalendar(row, field, ent)

    return ent


def createHalf(frame, field, side):
    row = Frame(frame)
    ent = createGenEntry(row, field, side)
    row.pack(side=LEFT, fill=X, expand=1, anchor=W)
    return ent


def makeform(window, fields):
    entries = {}

    # Create first row

    topframe1 = Frame(window)
    topframe1.pack(fill=X, expand=1, anchor=N)
    top1_1 = Frame(topframe1)
    top1_1.pack(fill=X, expand=1, anchor=W)
    half1_1 = Frame(topframe1)
    half1_1.pack(fill=X, expand=1, anchor=W)
    half1_2 = Frame(topframe1)
    half1_2.pack(fill=X, expand=1, anchor=W)

    topframe2 = Frame(window)
    topframe2.pack(fill=X, expand=1, anchor=N)
    top2_1 = Frame(topframe2)
    top2_1.pack(fill=X, expand=1, anchor=W)
    half2_1 = Frame(topframe2)
    half2_1.pack(fill=X, expand=1, anchor=W)

    topframe3 = Frame(window)
    topframe3.pack(fill=X, expand=1, anchor=N)
    top3_1 = Frame(topframe3)
    top3_1.pack(fill=X, expand=1, anchor=W)
    half3_1 = Frame(topframe3)
    half3_1.pack(fill=X, expand=1, anchor=W)

    topframe4 = Frame(window)
    topframe4.pack(fill=X, expand=1, anchor=N)

    i = 0
    for field in fields:
        i += 1

        # Create top section
        if i <= 5:
            if i == 1:  # "Full Legal Name"
                ent = createGenEntry(top1_1, field, TOP)
                entries[field] = ent
                continue
            ent = createHalf(half1_1, field, RIGHT)
            entries[field] = ent
        elif i <= 7:
            ent = createHalf(half1_2, field, RIGHT)
            entries[field] = ent
        # Create next section
        elif i <= 11:
            if i == 8:
                ent = createGenEntry(top2_1, field, TOP)
                entries[field] = ent
                continue
            ent = createHalf(half2_1, field, RIGHT)
            entries[field] = ent
        # Create Third Secontion with ("Current Full Address" up to "Landlord PN")
        elif i <= 18:
            if i == 12:
                ent = createHalf(top3_1, field, TOP)
                entries[field] = ent
                continue
            ent = createHalf(half3_1, field, RIGHT)
            entries[field] = ent
    return entries


"""
def makeform(window, fields):
    entries = {}
    regLetters = window.register(db.verifyForLetters)
    regNum = window.register(db.verifyForNumbers)

    for field in fields:
        row = Frame(window)
        lab = Label(row, width=22, text=field + ": ", anchor="w")
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)

        if field == "Full Legal Name" or field == "Agent/Referred By":
            ent.config(validate="key", validatecommand=(regLetters, "%S"))
        if (
            field == "SSN"
            or field == "Drivers License"
            or field == "Home Phone Number"
            or field == "Work Phone Number"
        ):
            createNumberOnly(row, entries, field, regNum, ent)
        if field == "Date of Birth" or field == "Start of Rental Date":
            createTkCalendar(row, entries, field, ent)

        entries[field] = ent
    return entries
"""


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
