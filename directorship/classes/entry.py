
class Entry:
    """
    An Entry constructed from a .csv table.
    """

    def __init__(self, firm_id, firm_name, full_name, first, middle, last, suffix, address):

        self.firm_id = firm_id
        self.firm_name = firm_name
        self.address = address
        # Name Info
        self.full_name = full_name
        self.first = first
        self.first_init = first[0]
        if middle == "0":
            self.middle = ""
            self.middle_init = ""
            self.middle_void = True
        else:
            self.middle = middle
            self.middle_init = middle[0]
            self.middle_void = False
        self.last = last
        if suffix == "0":
            self.suffix = ""
            self.suffix_void = True
        else:
            self.suffix = suffix
            self.suffix_void = False
        self.is_first_init = len(self.first) == 1
        self.is_middle_init = len(self.middle) == 1

    def __repr__(self):
        return "Entry<{} {}>".format(self.firm_id, self.full_name)

    def __str__(self):
        return "<{} | {}>".format(self.firm_id, self.full_name)

    def get_director_constructor(self):
        return [self.first, self.middle, self.last, self.suffix, self]


