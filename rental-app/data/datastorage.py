#!/usr/bin/env python3
# Handles form data and storage

from openpyxl import *
from pandas import *

# import pandas as pd

filepath = "workbook.xlsx"

# TODO: Work on create cvs sheet
def createExcel(ent):
    print("Creating spreadsheet...")
    wb = Workbook()
    sheet = wb.active
    sheet.append(ent)
    wb.save(filepath)


# TODO: Create data verification function
#       [] Must be able to check if all fields contain something in them
#       [] Must be able to check if the data in the fields are valid
# DONE: Create data saving function
#       [x] Must be able to retrieve the data from each entry
#       [x] Populate each data into the respective header in CVS sheet


def getValues(ent):
    values = []
    temp = []
    for x in ent:
        temp.append(str(ent[x].get()))
    values = temp
    return values


def saveValues(ent):
    values = getValues(ent)
    # print(values)
    wb = load_workbook(filepath)
    sheet = wb.active
    sheet.append(values)
    wb.save(filepath)
