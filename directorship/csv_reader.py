import csv
from .classes.firm import Firm
from .classes.entry import Entry

###########################################################
#  Change these values depending on the .csv being read.  #
###########################################################


FIRM_NAME_COL = 0
FIRST_COL = 1
MIDDLE_COL = 2
LAST_COL = 3
SUFFIX_COL = 4
FIRM_ID_COL = 5
FULL_NAME_COL = 6
ADDRESS_COL = 7

"""
FIRM_ID_COL = 5
FIRM_NAME_COL = 0
FULL_NAME_COL = 6
FIRST_COL = 1
MIDDLE_COL = 2
LAST_COL = 3
SUFFIX_COL = 4
ADDRESS_COL = 7
"""

###################################
#  DO NOT CHANGE BELOW THIS LINE  #
###################################


def read_csv(path):
    csv_file = open(path, newline='')
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # ignore header row
    firm_map = {}
    entries = []
    for row_values in csv_reader:

        # retrieve values from csv
        try:
            firm_id = row_values[FIRM_ID_COL]
            firm_name = row_values[FIRM_NAME_COL]
            full_name = row_values[FULL_NAME_COL]
            first = row_values[FIRST_COL]
            middle = row_values[MIDDLE_COL]
            last = row_values[LAST_COL]
            suffix = row_values[SUFFIX_COL]
            address = row_values[ADDRESS_COL]
        except IndexError:
            raise IndexError("At least one index value in csv_reader.py is out of bounds for given input csv.\n"
                             "Current Indices:\n"
                             "\tfirm id = {}\n"
                             "\tfirm name = {}\n"
                             "\tfull name = {}\n"
                             "\tfirst name = {}\n"
                             "\tmiddle name = {}\n"
                             "\tlast name = {}\n"
                             "\tsuffix = {}\n"
                             "\taddress = {}".format(FIRM_ID_COL, FIRM_NAME_COL, FULL_NAME_COL, FIRST_COL,
                                                     MIDDLE_COL, LAST_COL, SUFFIX_COL, ADDRESS_COL))

        # construct entry
        entry = Entry(firm_id, firm_name, full_name, first, middle, last, suffix, address)
        entries.append(entry)

        # add firm to firm_map
        if firm_id not in firm_map:
            firm = Firm(firm_name, firm_id)
            firm_map[firm_id] = firm

    return entries, firm_map
