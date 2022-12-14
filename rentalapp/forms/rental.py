"""Generates the rental application form"""

from tkinter import *
from tkcalendar import DateEntry
import data.datastorage as db
from datetime import datetime

# Variable Declaration
mainWindow = Tk()

# This variable is used for declaring the fields to be generated for the form
# 18 elements in total
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
)


def saveAndClose(ent, win):
    """Function to take data from GUI window and write to an excel file

    Parameters
    ----------
    ent : List
        The list of data to be processed

    win : Tk
        The primary application window in which to get the data from

    """
    db.saveValues(ent, win)


def createNumberOnly(frame, field, reg, old_ent):
    """Function creates Entries that only take numeric characters

    Parameters
    ----------
    frame : Tk
        The frame in which to place the elements into
    field : List
        The list of entry names to create Entry boxes for
    reg : Callable Function
        The callable function to be used for validating the Entry boxes
    old_ent : Entry
        The original Entry box that will be removed

    """
    old_ent.pack_forget()  # Kill original entry
    text = StringVar()
    ent = Entry(frame, textvariable=text)

    ent.config(textvariable=text, validate="key", validatecommand=(reg, "%S"))
    if field == "SSN" or field == "Drivers License":
        text.trace("w", lambda *args: db.characterLimit(text, 9))
    elif field.find("PN"):
        text.trace("w", lambda *args: db.characterLimit(text, 10))
    ent.pack(side=RIGHT, expand=YES, fill=X)

    return ent


def createTkCalendar(frame, field, old_ent):
    """Function that creates the calendar entry for Date of Birth

    Parameters
    ----------
    frame : Tk
        The frame in which to place the elements into
    field : List
        The list of entry names to create Entry boxes for
    old_ent : Entry
        The original Entry box that will be removed

    """
    old_ent.pack_forget()
    cal = DateEntry(frame)
    # Make entries that are rental start dates not limited to have minimal date at today's date
    if not field == "Start of Rental":
        cal = DateEntry(frame, selectmode="day", date_pattern="mm/dd/y")
    else:
        cal = DateEntry(
            frame, selectmode="day", mindate=datetime.now(), date_pattern="mm/dd/y"
        )
    cal.delete(0, "end")
    cal.pack(side=RIGHT, expand=YES, fill=X)
    return cal


def createGenEntry(frame, field, loc):
    """Creates generic Entry boxes with labels

    Main function that creates generic Entries and all variations of Entry types
    (like DateTime entries, Number only entries, and Letter only entries)

    Parameters
    ----------
    frame : Tk
        The frame in which to place the elements into
    field : List
        The list of entry names to create Entry boxes for
    loc : Side
        The location in which to orenate the Frame that holds the Entry box and Label

    """
    regLetters = frame.register(
        db.allowOnlyLetters
    )  # Create register function for checking entry characters (letters/specific symbols only type)
    regNum = frame.register(
        db.allowOnlyNumbers
    )  # Create register function for checking entry characters (numbers only type)
    row = Frame(frame)
    lab = Label(row, text=field + ": ", anchor="w")
    ent = Entry(row)
    row.pack(side=loc, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)

    # Makes these entries within statement only accept letters and specific symbols
    if (
        field == "Full Legal Name"
        or field == "Agent/Referred By"
        or field == "Landlord"
    ):
        ent.config(validate="key", validatecommand=(regLetters, "%S"))

    # Makes these entries within statement only accept numeric characters
    if (
        field == "SSN"
        or field == "Drivers License"
        or field == "Home PN"
        or field == "Work PN"
        or field == "Landlord PN"
        or field == "Proposed Rent"
        or field == "Current Rent"
    ):
        ent = createNumberOnly(row, field, regNum, ent)

    # Makes these entries within statement use Date Entries
    if (
        field == "Date of Birth"
        or field == "Start of Rental"
        or field == "Date In"
        or field == "Date Out"
    ):
        ent = createTkCalendar(row, field, ent)

    return ent


def createHalf(frame, field, side):
    """Create an Entry within a frame used in a half of an entire section frame

    # Create an Entry within a half section frame, picking the orentation of the
    # newly created frame and entry

    Parameters
    ----------
    frame : Tk
        The frame in which to place the elements into
    field : List
        The list of entry names to create Entry boxes for
    side : Side
        The location in which to orenate the Frame that holds the Entry box and Label

    """
    row = Frame(frame)
    ent = createGenEntry(row, field, side)
    row.pack(side=LEFT, fill=X, expand=1, anchor=W)
    return ent


def makeform(window, fields):
    """Creates all gui elements of the form

    Creates all of the necessary elements of the form, then places them into the
    form's applicaiton window

    Parameters
    ----------
    window : Tk
        The application window to use to place all of the elements into
    fields : List
        The list of entry names to create the form with

    """
    entries = {}  # Empty list, usd to save all entries created

    # Create first section of the form (Renter's Personal Data)
    topframe1 = Frame(window)  # Primary frame for the section, holds all other frames
    topframe1.pack(fill=X, expand=1, anchor=N)
    top1_1 = Frame(topframe1)  # Top Row of the section
    top1_1.pack(fill=X, expand=1, anchor=W)
    half1_1 = Frame(topframe1)  # First Half of the section
    half1_1.pack(fill=X, expand=1, anchor=W)
    half1_2 = Frame(topframe1)  # Second half of the section
    half1_2.pack(fill=X, expand=1, anchor=W)

    # Create second section of the form (Rental Property Data)
    topframe2 = Frame(window)  # Primary frame for the section, holds all other frames
    topframe2.pack(fill=X, expand=1, anchor=N)
    top2_1 = Frame(topframe2)  # Top Row for the section
    top2_1.pack(fill=X, expand=1, anchor=W)
    half2_1 = Frame(topframe2)  # Half of the section
    half2_1.pack(fill=X, expand=1, anchor=W)

    # Create third section of the form (Previous History Data)
    topframe3 = Frame(window)  # Primary frame for the section, holds all other frames
    topframe3.pack(fill=X, expand=1, anchor=N)
    top3_1 = Frame(topframe3)  # Top Row for the section
    top3_1.pack(fill=X, expand=1, anchor=W)
    half3_1 = Frame(topframe3)  # Half of the section
    half3_1.pack(fill=X, expand=1, anchor=W)

    i = 0  # Used for selecting entries based on its index, used for skipping elements
    for field in fields:
        i += 1  # Start counting up, assosicated the elem's index to a value of i

        # Create Renter Personal Data section
        if i <= 5:  # First 5 elements
            if i == 1:  # Make element 1 (Full Legal Name) the top row of the section
                ent = createGenEntry(top1_1, field, TOP)
                entries[field] = ent  # Add entries to entry list
                continue
            ent = createHalf(
                half1_1, field, RIGHT
            )  # Create the half section with elements 2 - 5
            entries[field] = ent  # Add entries to entry list
        elif i <= 7:  # Elements after the first 5
            ent = createHalf(
                half1_2, field, RIGHT
            )  # Create the half section with elements 6 - 7
            entries[field] = ent  # Add entries to entry list
            #
        # Create Rental Property Data Section
        elif i <= 11:  # Grab elements from 8 to 11
            if i == 8:  # Make element 8 (Property Address) the top row of the section
                ent = createGenEntry(top2_1, field, TOP)
                entries[field] = ent  # Add entries to entry list
                continue
            ent = createHalf(
                half2_1, field, RIGHT
            )  # Create the half section with elements 9 - 11
            entries[field] = ent  # Add entries to entry list

        # Create Previous History Data Section Third Secontion
        elif (
            i <= 18
        ):  # Grab elements 12 yo 18 ("Current Full Address" up to "Landlord PN")
            if (
                i == 12
            ):  # Make element 12 (Current Full Address) the top row of the section
                ent = createHalf(top3_1, field, TOP)
                entries[field] = ent  # Add entries to entry list
                continue
            ent = createHalf(
                half3_1, field, RIGHT
            )  # Create the half section with elements 13 - 18
            entries[field] = ent  # Add entries to entry list

    return entries  # Return all entries placed in the entries list


def createRentalForm():
    """Runs everything to create the entire application"""
    # Create Window
    mainWindow.geometry("")  # Make window geometry autosize
    mainWindow.title("Rental Application Form")

    ents = makeform(
        mainWindow, fields
    )  # Create the entires and save them as a list, used for data saving

    # create a Submit Button and place into the root window
    submit = Button(
        mainWindow,
        text="Submit",
        fg="White",
        bg="Red",
        command=(lambda e=ents: saveAndClose(e, mainWindow))).pack(side=LEFT, padx=5, pady=5)

    # Start form
    mainWindow.mainloop()
