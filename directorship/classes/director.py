
class Director:

    log_writer = None

    def __init__(self, first, middle, last, suffix, entry):

        self.first = first
        self.is_first_init = len(first) == 1
        self.middle = middle
        self.is_middle_init = len(middle) == 1
        self.last = last
        self.suffix = suffix

        self.firms = set()
        self.entries = [entry]

        self.flagged_for_duplicate_entry = False

    def __repr__(self):
        return "Director<{}>".format(str(self))

    def __str__(self):
        full_name = self.first
        if self.middle:
            full_name += " " + self.middle
        if self.last:
            full_name += " " + self.last
        if self.suffix:
            full_name += " " + self.suffix
        return full_name

    def associate_with_entry(self, e):
        if len(e.first) > len(self.first):
            self.first = e.first
            self.is_first_init = len(self.first) == 1
        if len(e.middle) > len(self.middle):
            self.middle = e.middle
            self.is_middle_init = len(self.middle) == 1
        self.entries.append(e)

    def add_firm(self, firm):
        if firm not in self.firms:
            self.firms.add(firm)
        else:
            if not self.flagged_for_duplicate_entry:
                self.log_writer.write_directors_to_file(self.log_writer.LIST_DUPLICATE_FIRM_ADDED, [self])
                self.flagged_for_duplicate_entry = True

    def get_num_links(self, other_director):
        return len(self.firms.intersection(other_director.firms))

    def get_adj_matrix_ref(self):
        aliases = [e.full_name for e in self.entries]
        max_length = max([len(a) for a in aliases])
        return [a for a in aliases if len(a) == max_length][0]

    def get_aliases(self):
        return {e.full_name for e in self.entries}

    def get_info(self):
        return "{}" \
               "\n\taliases: {}" \
               "\n\tentries: {}" \
               "\n\taddresses: {}" \
               "\n\n".format(str(self),
                             ", ".join({e.full_name for e in self.entries}),
                             ", ".join([str(e) for e in self.entries]),
                             ", ".join({e.address for e in self.entries})
                             )

    def merge(self, other_director):
        assert self.middle, "Director does not have a middle name and is trying to merge"
        assert not other_director.middle, "Director to be merged has a middle name"
        if len(self.firms.intersection(other_director.firms)) == 0:
            self.log_writer.write_merged_directors(self, other_director)
            for e in other_director.entries:
                self.associate_with_entry(e)
            while len(other_director.firms) > 0:
                f = other_director.firms.pop()
                f.directors.remove(other_director)
                self.add_firm(f)
            self.log_writer.write_result_from_merge(self)
            return True
        else:
            self.log_writer.write_bad_merge_directors(self, other_director)
            return False

    def remove_from_firms(self):
        while len(self.firms) > 0:
            f = self.firms.pop()
            f.directors.remove(self)

    @staticmethod
    def set_log_writer(log_writer):
        Director.log_writer = log_writer
