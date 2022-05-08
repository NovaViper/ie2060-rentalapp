#!/usr/bin/env python3

"""Primary launcher function, executing the entire program

    Examples
    --------
    Run the script with 'python rentalapp'

"""

import forms.rental as rental
import data.datastorage as data
import os.path as path

if __name__ == "__main__":
    if not (path.isfile(data.filepath)):
        data.createWorkBook(rental.fields)
    rental.createRentalForm()
