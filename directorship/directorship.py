import os
import sys
import argparse
from .classes.graph import Graph
from .classes.director import Director
from .csv_reader import read_csv
from .csv_writer import write_graph_to_csv, write_aliases_to_csv
from .entry_handler import get_directors
from .log_writer import LogWriter

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input csv file located in data/input/')
    parser.add_argument('output', help='name of output directory to create or overwrite in data/output/')
    parser.add_argument('-f', action='store_true', help='write firm edge list')
    parser.add_argument('-d', action='store_true', help='write director edge list')
    parser.add_argument('-a', action='store_true', help='write aliases')
    parser.add_argument('--indir', type=str, default='data/input')
    parser.add_argument('--outdir', type=str, default='data/output')
    return parser.parse_args(args)

def main(args):
    # parse arguments from the command line
    input_file = args.input  # csv in data directory to be read
    output_directory_name = args.output  # name of output directory to be created
    write_firms_edge_list = args.f  # write firms edge list or not
    write_directors_edge_list = args.d  # write directors edge list or not
    write_aliases = args.a  # write director aliases

    input_path = f"{args.indir}/{input_file}"
    output_directory = f"{args.outdir}/{output_directory_name}/"

    output_log_directory = output_directory + "logs/"
    output_firms_edge_list_path = output_directory + "firms_edge_list.csv"
    output_directors_edge_list_path = output_directory + "directors_edge_list.csv"
    output_aliases_list_path = output_directory + "aliases.csv"

    # check and correct directory structure
    os.makedirs(args.indir, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(output_log_directory, exist_ok=True)

    # check existence of input file
    if not os.path.isfile(input_path):
        sys.exit("Operation aborted. Input file '{}' does not exist.".format(input_path))

    # ask user to continue, warn about overwrite
    user_continue = input("The directory {} will be overwritten. Continue? [yes/no] ".format(
        output_directory)).lower()
    if user_continue != "yes":
        sys.exit("Operation aborted by user.")

    # initialize logs
    print("* Initializing logs")
    log_writer = LogWriter(output_log_directory)
    log_writer.initialize_text_files()
    Director.set_log_writer(log_writer)

    # read input csv
    print("* Reading '{}'".format(input_path))
    try:
        entries, firm_map = read_csv(input_path)
    except IndexError as e:
        sys.exit("Error reading file {}: {}".format(input_path, e))

    # build director and firm lists
    print("* Constructing Directors and Firms")
    directors = get_directors(entries, firm_map, log_writer)
    firms = list(firm_map.values())

    # write counts to logs
    log_writer.write_counts()

    # write firm edge list
    if write_firms_edge_list:
        print("* Writing Firm Edge List to '{}'".format(output_firms_edge_list_path))
        firm_graph = Graph(firms)
        write_graph_to_csv(output_firms_edge_list_path, firm_graph)

    # write director edge list
    if write_directors_edge_list:
        print("* Writing Director Edge List to '{}'".format(output_directors_edge_list_path))
        directors_graph = Graph(directors)
        write_graph_to_csv(output_directors_edge_list_path, directors_graph)

    if write_aliases:
        print("* Writing aliases to '{}' ".format(output_aliases_list_path))
        write_aliases_to_csv(output_aliases_list_path, directors)

    print("Success. Logs written to '{}'".format(output_log_directory))


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
