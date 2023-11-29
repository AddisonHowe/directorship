
class LogWriter:

    def __init__(self, log_directory):
        self.output_directory = log_directory
        self.LIST_SINGLETONS = log_directory + "singletons.txt"
        self.LIST_NON_SINGLETONS = log_directory + "non singletons.txt"
        self.LIST_MIDDLE = log_directory + "middle name present.txt"
        self.LIST_NO_MIDDLE = log_directory + "no middle name present.txt"
        self.LIST_NO_MIDDLE_FIRST_FULL = log_directory + "no middle name and first name full.txt"
        self.LIST_NO_MIDDLE_FIRST_INITIAL = log_directory + "no middle name and first name initial.txt"
        self.LIST_MIDDLE_SINGLETONS = log_directory + "middle name singletons.txt"
        self.LIST_MIDDLE_NON_SINGLETONS = log_directory + "middle name non singletons.txt"
        self.LIST_MIDDLE_NON_SINGLETONS_UNAMBIGUOUS = log_directory + "middle name non singletons unambiguous.txt"
        self.LIST_MIDDLE_NON_SINGLETONS_AMBIGUOUS = log_directory + "middle name non singletons ambiguous.txt"
        self.LIST_AMBIGUOUS_DUAL_INITIAL_CULPRIT = log_directory + "ambiguous dual initial culprits.txt"
        self.LIST_AMBIGUOUS_DUAL_INITIAL_NON_CULPRIT = log_directory + "ambiguous dual initial non culprits.txt"
        self.LIST_UNAMBIGUOUS_WITH_DUAL_INITIAL_REMOVED = log_directory + "unambiguous with dual initial removed.txt"
        self.LIST_TRULY_AMBIGUOUS = log_directory + "truly ambiguous.txt"
        self.LIST_DUPLICATE_FIRM_ADDED = log_directory + "duplicate firm added.txt"
        self.LIST_ALL_DIRECTORS = log_directory + "all directors.txt"
        self.LIST_MERGED_DIRECTORS = log_directory + "merged directors.txt"
        self.LIST_BAD_MERGE_DIRECTORS = log_directory + "bad merge attempted directors.txt"
        self.LIST_DIRECTORS_CONSTRUCTED_FROM_DUPLICATE_FIRM_ISSUE = log_directory + "dirs from duplicate firm issue.txt"

        self.LISTS = {
            self.LIST_SINGLETONS: 0,
            self.LIST_NON_SINGLETONS: 1,
            self.LIST_MIDDLE: 2,
            self.LIST_NO_MIDDLE: 3,
            self.LIST_NO_MIDDLE_FIRST_FULL: 4,
            self.LIST_NO_MIDDLE_FIRST_INITIAL: 5,
            self.LIST_MIDDLE_SINGLETONS: 6,
            self.LIST_MIDDLE_NON_SINGLETONS: 7,
            self.LIST_MIDDLE_NON_SINGLETONS_UNAMBIGUOUS: 8,
            self.LIST_MIDDLE_NON_SINGLETONS_AMBIGUOUS: 9,
            self.LIST_AMBIGUOUS_DUAL_INITIAL_CULPRIT: 10,
            self.LIST_AMBIGUOUS_DUAL_INITIAL_NON_CULPRIT: 11,
            self.LIST_UNAMBIGUOUS_WITH_DUAL_INITIAL_REMOVED: 12,
            self.LIST_TRULY_AMBIGUOUS: 13,
            self.LIST_DUPLICATE_FIRM_ADDED: 14,
            self.LIST_ALL_DIRECTORS: 15,
            self.LIST_MERGED_DIRECTORS: 16,
            self.LIST_BAD_MERGE_DIRECTORS: 17,
            self.LIST_DIRECTORS_CONSTRUCTED_FROM_DUPLICATE_FIRM_ISSUE: 18
        }

        self.COUNTS = [0 for _ in range(len(self.LISTS))]

    def write_directors_to_file(self, path, directors):
        self.COUNTS[self.LISTS[path]] += len(directors)
        directors.sort(key=lambda d: (d.last, d.first, d.middle, d.suffix))
        file = open(path, 'a')
        for director in directors:
            file.write(director.get_info())
        file.close()

    def write_merged_directors(self, director_with_middle, director_wo_middle):
        self.COUNTS[self.LISTS[self.LIST_MERGED_DIRECTORS]] += 1
        file = open(self.LIST_MERGED_DIRECTORS, 'a')
        file.write(director_wo_middle.get_info())
        file.write("MERGED WITH\n")
        file.write(director_with_middle.get_info())
        file.close()

    def write_result_from_merge(self, director):
        file = open(self.LIST_MERGED_DIRECTORS, 'a')
        file.write("RESULTING DIRECTOR\n")
        file.write(director.get_info())
        file.write("*------------------------------------------*\n")
        file.close()

    def write_bad_merge_directors(self, director_with_middle, director_wo_middle):
        self.COUNTS[self.LISTS[self.LIST_BAD_MERGE_DIRECTORS]] += 1
        file = open(self.LIST_BAD_MERGE_DIRECTORS, 'a')
        file.write(director_wo_middle.get_info())
        file.write("Could not be merged with\n")
        file.write(director_with_middle.get_info())
        file.write("*------------------------------------------*\n")
        file.close()

    def write_counts(self):
        for path in self.LISTS:
            with open(path, 'a') as f:
                f.write("\nCount: {}".format(self.COUNTS[self.LISTS[path]]))
                f.close()

    def initialize_text_files(self):
        with open(self.LIST_SINGLETONS, 'w') as f:
            f.write("List of Directors constructed from an entry with unique (First Initial, Last, Suffix)\n\n")
            f.close()
        with open(self.LIST_NON_SINGLETONS, 'w') as f:
            f.write("List of Directors constructed from entries without a unique (First Initial, Last, Suffix)\n\n")
            f.close()
        with open(self.LIST_MIDDLE, 'w') as f:
            f.write("List of Directors constructed from entries with a non-void Middle\n\n")
            f.close()
        with open(self.LIST_NO_MIDDLE, 'w') as f:
            f.write("List of Directors constructed from entries with a void Middle\n\n")
            f.close()
        with open(self.LIST_NO_MIDDLE_FIRST_FULL, 'w') as f:
            f.write("List of Directors constructed from entries with a void Middle and full First\n\n")
            f.close()
        with open(self.LIST_NO_MIDDLE_FIRST_INITIAL, 'w') as f:
            f.write("List of Directors constructed from entries with a void Middle and non-full First\n\n")
            f.close()
        with open(self.LIST_MIDDLE_SINGLETONS, 'w') as f:
            f.write("List of Directors constructed from an entry with a unique "
                    "(First Initial, Middle Initial, Last, Suffix)\n\n")
            f.close()
        with open(self.LIST_MIDDLE_NON_SINGLETONS, 'w') as f:
            f.write("List of Directors constructed from entries without a unique "
                    "(First Initial, Middle Initial, Last, Suffix)\n\n")
            f.close()
        with open(self.LIST_MIDDLE_NON_SINGLETONS_UNAMBIGUOUS, 'w') as f:
            f.write("List of Directors constructed from entries that are transitive "
                    "under the name equivalence relation\n\n")
            f.close()
        with open(self.LIST_MIDDLE_NON_SINGLETONS_AMBIGUOUS, 'w') as f:
            f.write("List of Directors constructed from entries that are not transitive "
                    "under the name equivalence relation\n\n")
            f.close()
        with open(self.LIST_AMBIGUOUS_DUAL_INITIAL_CULPRIT, 'w') as f:
            f.write("List of Directors with dual initials that are the cause of intransitivity "
                    "with otherwise transitive entries\n\n")
            f.close()
        with open(self.LIST_AMBIGUOUS_DUAL_INITIAL_NON_CULPRIT, 'w') as f:
            f.write("List of Directors with dual initials that are NOT the cause of "
                    "intransitivity with intransitive entries\n\n")
            f.close()
        with open(self.LIST_UNAMBIGUOUS_WITH_DUAL_INITIAL_REMOVED, 'w') as f:
            f.write("List of Directors with at least one of First or Middle Full, "
                    "that are transitive when dual initial entries removed \n\n")
            f.close()
        with open(self.LIST_TRULY_AMBIGUOUS, 'w') as f:
            f.write("List of Directors with at least one of First or Middle Full, "
                    "that remain intransitive when dual initial entries removed \n\n")
            f.close()
        with open(self.LIST_DUPLICATE_FIRM_ADDED, 'w') as f:
            f.write("List of Directors for which a duplicate firm was added \n\n")
            f.close()
        with open(self.LIST_ALL_DIRECTORS, 'w') as f:
            f.write("List of all Directors constructed\n\n")
            f.close()
        with open(self.LIST_MERGED_DIRECTORS, 'w') as f:
            f.write("List of Directors that were merged together\n\n")
            f.close()
        with open(self.LIST_BAD_MERGE_DIRECTORS, 'w') as f:
            f.write("List of Directors that could not be merged because they sit on the same board\n\n")
            f.close()
        with open(self.LIST_DIRECTORS_CONSTRUCTED_FROM_DUPLICATE_FIRM_ISSUE, 'w') as f:
            f.write("List of Directors that were constructed from a director flagged "
                    "for association with duplicate firms\n\n")
            f.close()
