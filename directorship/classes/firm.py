
class Firm:

    def __init__(self, name, firm_id):
        self.name = name
        self.firm_id = firm_id
        self.directors = set()

    def __str__(self):
        return self.firm_id

    def add_director(self, director):
        self.directors.add(director)

    def get_directors(self):
        return self.directors

    def get_adj_matrix_ref(self):
        return self.firm_id

    def get_num_links(self, other_firm):
        return len(self.directors.intersection(other_firm.directors))






