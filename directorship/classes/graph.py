
class Graph:

    def __init__(self, object_list):
        self.objects = object_list
        self.size = len(object_list)

    def get_value(self, r, c):
        obj1 = self.objects[r]
        obj2 = self.objects[c]
        return obj1.get_num_links(obj2)

    def get_references(self):
        return [o.get_adj_matrix_ref() for o in self.objects]

    def get_reference(self, r):
        return self.objects[r].get_adj_matrix_ref()

    def get_size(self):
        return self.size
