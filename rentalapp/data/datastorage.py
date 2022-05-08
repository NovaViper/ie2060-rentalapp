"""Contains functions for handling data from the forms and database storage"""

from tkinter import messagebox as message
from openpyxl import *
import re

# Filepath for spreadhseet database
filepath = "workbook.xlsx"


def autoSizeColumns(worksheet):
    """Auto resizes spreadsheet columns to fit the data within them

    Parameters
    ----------
    worksheet : List
        The spreadsheet which is to be resized

    """
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column].width = adjusted_width


def createWorkBook(header):
    """Create a new Excel Spreadsheet for storing data

    Parameters
    ----------
    header : List
        The list that contains the headers to be added to the first row of the
        spreadsheet database

    """
    print("Creating database...")
    wb = Workbook()  # Create Workbook
    sheet = wb.active
    sheet.append(header)
    autoSizeColumns(sheet)
    wb.save(filepath)
    print("Done")


def getValues(ent):
    """Retrieves the values from a list

    Parameters
    ----------
    ent : List
        The list in which to retrieve data from

    """
    values = []
    temp = []
    for x in ent:
        temp.append(str(ent[x].get()))
    values = temp
    return values


def saveValues(array, window):
    """Verifies if data is valid, then saves it to the spreadsheet database if so

    Parameters
    ----------
    array : List
        The list of data to be saved and validated
    window : TKWindow
        The form to be closed

    """
    values = getValues(array)
    if verifyAll(values):  # Run Verification tests, and if pass then continue
        print("Submitting")
        wb = load_workbook(filepath)
        sheet = wb.active
        sheet.append(values)
        autoSizeColumns(sheet)
        wb.save(filepath)
        print("Done, I will end now")
        window.destroy()  # Kill the form


def verifyAll(data):
    """Verify a list of data

    Main function for verifying the collected data, if any of the verification
    tests fail, then show a warning message about the specific type of failure

    Parameters
    ----------
    data : List
        The list of data to be verified

    """

    #  If any values are empty, skip "Work PN" field because that can be null
    if checkForNull(data, 4):
        message.showwarning("Warning", "You haven't filled out all forms")
        return False
    # Check if the email address field is formatted correctly
    elif not verifyEmail(data[4]):
        message.showwarning(
            "Warning",
            "You have formatted your email address wrong, it should follow the format:\n- The format must be username@company.domain format\n- Username can only contain upper and lowercase letters, numbers, dashes and underscores\n- Company name can only contain upper and lowercase letters and numbers\n- Domain can only contain upper and lowercase letter.\n- Maximum length of the extension is 3.")
        return False

    # Check if the SSN is the correct length
    elif not (verifyNumLength(data[5], 9, 0)):
        message.showwarning(
            "Warning",
            "You have entered an invalid social security number, please check your data")
        return False

    # Check if the Drivers License is the correct length
    elif not (verifyNumLength(data[6], 9, 0)):
        message.showwarning(
            "Warning",
            "You have entered an invalid driver's license number, please check your data")
        return False

    # Check if the Phone Numbers are the correct length
    elif not (verifyNumLength(data[2], 10, 0)):
        message.showwarning(
            "Warning",
            "You have entered an invalid home phone number, please check your data")
        return False

    elif not (verifyNumLength(data[17], 10, 0)):
        message.showwarning(
            "Warning",
            "You have entered an invalid landlord phone number, please check your data")
        return False

    # Check if the Work Phone Number is the correct length, accounts for when it is null
    elif not (verifyNumLength(data[3], 10, 1)):
        message.showwarning(
            "Warning",
            "You have entered an invalid work phone number, please check your data")
        return False
    # Check if the Property Street Address is in valid format
    elif not (verifyStreetAddress(data[7])):
        message.showwarning(
            "Warning",
            "You have entered an invalid property street address, please check your data. The format should be: Street Address, City, StateInitals ZipCode")
        return False

    # Check if the Current Street Address is in valid format
    elif not (verifyStreetAddress(data[11])):
        message.showwarning(
            "Warning",
            "You have entered an invalid current street address, please check your data. The format should be: Street Address, City, StateInitals, ZipCode")
        return False
    else:  # If everything is valid
        return True


def allowOnlyLetters(data):
    """Only allow letters, spaces, or symbols such as "'" and "-" to be entered in an Entry field

    Parameters
    ----------
    data : String
        The data to be checked

    """
    return data.isalpha() or data == "'" or data == "-" or data.isspace()


def allowOnlyNumbers(data):
    """Only allow numbers to be entered in an Entry field

    Parameters
    ----------
    data : String
        The data to be checked

    """
    return data.isdigit()


def verifyNumLength(data, length, nullable: int):
    """Verify if data in Entry field is the correct length

    Verify if data in Entry field is the correct length, if the data is a
    nullable type (if nullable is 1), then an empty length of 0 is also valid
    but anything more than 0 but less than the specified length is not valid

    Parameters
    ----------
    data : String
        The data to be checked
    length : int
        The length the data should be
    nullable : int
        Flag to allow for null values for a specific data entry

    """
    if len(data) == length and nullable == 0:
        return True
    if len(data) == length and nullable == 1:
        return True
    if len(data) == 0 and nullable == 1:
        return True
    return False


# Verify if data in an Entry field is properly formatted as an email address
def verifyEmail(data):
    """Verify if the data in an Entry field is properly formatted as an email address

    The format must be username@company.domain format
        - Username can only contain upper and lowercase letters, numbers, dashes and underscores
        - Company name can only contain upper and lowercase letters and numbers
        - Domain can only contain upper and lowercase letters
        - Maximum length of the extension is 3.

    Parameters
    ----------
    data : String
        The data to be processed

    """
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, data):
        return True
    return False


def verifyStreetAddress(data):
    """Verify if data in entry field is properly formatted as a street address

    Parameters
    ----------
    data : String
        The data to be processed

    Valid Examples
    --------
    123 test st, test city, TT 12345
    859 Squaw Creek Avenue, Baltimore, MD 21206
    3333 Josephine AVE #114, Temecula, CA 99999
    3636 Nicholson Dr, Baton Rouge, LA 70802
    7912 S Willow Drive, Redford, MI 48239

    """
    regex = r"\d{1,6}\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s*[A-Z]{2}\s*\d{5}"

    regex = re.compile(regex)
    match = regex.match(data)
    if match:
        return True
    else:
        return False


def checkForNull(fields, skip: int):
    """Check if an array list fields contains any empty values

    Parameters
    ----------
    fields : List
        The list of Entry fields to be checked
    skip : int
        The index value to allow for null values

    """
    i = 0  # Used for selecting entries based on its index, used for skipping elements
    values = []
    for elem in fields:
        i += 1  # Start counting up, assosicated the elem's index to a value of i
        if i == skip:
            continue
        values.append(elem)
    result = any([isEmptyOrBlank(elem) for elem in values])
    return result


def isEmptyOrBlank(msg):
    """Check if given string is empty or contains only white spaces, for checkForNull function

    Parameters
    ----------
    msg :
        The element to be processed

    """
    return re.search("^\s*$", msg)


def characterLimit(text, length):
    """Limit a string to a certain length, used for limiting the number of allowed characters in an Entry field

    Parameters
    ----------
    text : String
        The text to be processed
    length : int
        The length to limit the text to

    """
    if len(text.get()) > length:
        text.set(text.get()[:length])
