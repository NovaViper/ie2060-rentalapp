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
    if not (path.isfile(data.filepath)):
        data.createExcel(rental.fields)
    rental.createRentalForm()
