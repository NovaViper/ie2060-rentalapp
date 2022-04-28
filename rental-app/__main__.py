#!/usr/bin/env python3
# Primary launcher function, run the script with 'python rental-app'

# Open Applications
# Submit Applications
# Save Application Data

import forms.lease as lease
import forms.rental as rental
import data.datastorage as data
import os.path as path

if __name__ == "__main__":

    # if not (path.isfile(data.filepath)):
    #    data.createDatabase(rental.fields)
    # else:
    #    data.loadcreateDatabase()
    if not (path.isfile(data.filepath)):
        data.createWorkBook(rental.fields)
    rental.createRentalForm()
