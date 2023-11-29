import csv

def write_graph_to_csv(path, graph):

    file = open(path, mode='w')
    writer = csv.writer(file)

    # Write Rows
    size = graph.get_size()
    for i in range(size - 1):
        if i % 100 == 0:
            print("\tWriting row {} of {}".format(i, size))
        for j in range(i + 1, size):
            value = graph.get_value(i, j)
            if value > 0:
                ref1 = graph.get_reference(i)
                ref2 = graph.get_reference(j)
                row_to_write = [ref1, ref2]
                for _ in range(value):
                    writer.writerow(row_to_write)
    file.close()


def write_aliases_to_csv(path, directors):
    count_map = {}
    file = open(path, mode='w')
    writer = csv.writer(file)
    for d in directors:
        aliases = d.get_aliases()
        num_aliases = len(aliases)
        if num_aliases not in count_map:
            count_map[num_aliases] = 0
        count_map[num_aliases] += 1
        writer.writerow(aliases)
    file.close()
