#!/usr/bin/env python3
# Handles form data and storage

from openpyxl import *

filepath = "workbook.xlsx"


def autoSizeColumns(worksheet):
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


def createWorkBook(ent):
    print("Creating database...")
    wb = Workbook()
    sheet = wb.active
    sheet.append(ent)  # Add All Entries to Spreadsheet
    autoSizeColumns(sheet)  # Resize spreadsheet column
    wb.save(filepath)
    print("Done")


# TODO: Create data verification function
#       [] Must be able to check if all fields contain something in them
#       [] Must be able to check if the data in the fields are valid


def getValues(ent):
    values = []
    temp = []
    for x in ent:
        temp.append(str(ent[x].get()))
    values = temp
    return values


def saveValues(ent):
    values = getValues(ent)
    # Verification
    # print(values)
    wb = load_workbook(filepath)
    sheet = wb.active
    sheet.append(values)
    autoSizeColumns(sheet)
    wb.save(filepath)


# Input Management
def verifyForLetters(data):
    return data.isalpha() or data == "'" or data == "-" or data.isspace()


def verifyForNumbers(data):
    return data.isdigit()


def verifyEmail(data):
    print("")


def character_limit(text, length):
    if len(text.get()) > length:
        text.set(text.get()[:length])
