from .classes.director import Director

def get_directors(entries, firm_map, log_writer):
    """Process entries and return list of directors.

    Entries are clustered into sets sharing a common
    First Initial, Last Name, and Jr Status. These sets are partitioned based on whether or not
    they contain a single entry. In the case of a singleton set, the set contains an entry that
    differs in at least one of the three fields from all others, and thus gives a definable
    director. This director is constructed from the entry and added to a list of directors to be
    returned. In the case of a non-singleton set, the set is processed by function
    get_directors_from_non_singleton_set, and the resulting list is merged with the list to return.

    :param log_writer: log_writer
    :param entries: A list of entries
    :param firm_map: Mapping from firm_id to Firm object
    :return: A list of Directors
    """
    # Construct a mapping from (first_init, last, suffix) to set of satisfying entries
    mapping = {}
    for e in entries:
        k = (e.first_init, e.last, e.suffix)
        if k not in mapping:
            mapping[k] = set()
        mapping[k].add(e)

    # Partition the sets into those that are singletons and those that aren't
    singleton_sets = {}
    non_singleton_sets = {}
    for k in mapping:
        entry_set = mapping[k]
        if len(entry_set) == 1:
            singleton_sets[k] = mapping[k]
        else:
            non_singleton_sets[k] = mapping[k]

    # Singleton sets contain a definable director
    directors_from_singleton_sets = []
    for singleton_set in singleton_sets.values():
        entry = singleton_set.pop()
        new_director = create_director_from_entry(entry, firm_map)
        directors_from_singleton_sets.append(new_director)

    # Non-singleton sets must be processed differently
    directors_from_non_singleton_sets = []
    for k in non_singleton_sets:
        s = non_singleton_sets[k]
        directors_from_non_singleton_sets += get_directors_from_non_singleton_set(s, firm_map, log_writer)

    log_writer.write_directors_to_file(log_writer.LIST_SINGLETONS, directors_from_singleton_sets)
    log_writer.write_directors_to_file(log_writer.LIST_NON_SINGLETONS, directors_from_non_singleton_sets)
    all_directors = directors_from_singleton_sets + directors_from_non_singleton_sets
    all_directors.sort(key=lambda d: (d.last, d.first, d.middle, d.suffix))
    log_writer.write_directors_to_file(log_writer.LIST_ALL_DIRECTORS, all_directors)
    return all_directors


def get_directors_from_non_singleton_set(entries, firm_map, log_writer):
    """Process a non-singleton set of entries sharing a common First Initial, Last Name, and Jr Status.
    
    Entries are partitioned into those with and without a middle name, and handled separately.
    Therefore if one entry has a middle name and another does not, they will never be matched.
    Possible cause of Type I error.

    :param log_writer: log writer
    :param entries: Set of entries S, where each entry has the same First Initial,
        Last Name, and Jr Status. Furthermore, |S| > 1.
    :param firm_map: Mapping from firm_id to Firm object
    :return: A list of Directors resulting from the entries. Each Director in the returned list
        will have the same First Initial, Last Name, and Jr Status.
    """
    # Partition the set into entries with and without middle name
    entries_with_middle, entries_without_middle = get_entries_with_and_without_middle(entries)
    directors_without_middle = get_directors_without_middle(entries_without_middle, firm_map, log_writer)
    directors_with_middle = get_directors_with_middle(entries_with_middle, firm_map, log_writer)
    # Write Directors to output text files
    log_writer.write_directors_to_file(log_writer.LIST_MIDDLE, directors_with_middle)
    log_writer.write_directors_to_file(log_writer.LIST_NO_MIDDLE, directors_without_middle)
    # Fix duplicate firm issues
    directors_without_middle = unlink_directors_with_duplicate_firms(directors_without_middle, firm_map, log_writer)
    directors_with_middle = unlink_directors_with_duplicate_firms(directors_with_middle, firm_map, log_writer)
    # Merge directors with and without middle names
    directors = merge_directors(directors_with_middle, directors_without_middle)
    return directors


def get_directors_without_middle(entries, firm_map, log_writer):
    """Process a set of entries without a middle name. 

    Entries are grouped by first name, with one group having just a first 
    initial. Each group with a full first name is regarded as a single director. 
    If one such group is constructed into a Director, then the initial group is 
    matched to this director. Otherwise, the initial group is ambiguous and a 
    new Director is constructed, with First Name just the initial.

    :param log_writer: log writer
    :param entries: Set of entries, where each entry has the same First Initial,
        Last Name, and Jr Status; and no Middle Name.
    :param firm_map: Mapping from firm_id to Firm object
    :return: A list of Directors resulting from the entries. Each Director in the returned list
        will have the same First Initial, Last Name, and Jr Status, and no Middle Name
    """

    # Partition into entries with and without a full first name
    entries_with_full_first, entries_without_full_first = get_entries_with_and_without_full_first(entries)

    # Deal with entries with a full first name
    # Construct mapping from first name to set of entries with that name
    first_map = {}
    for e in entries_with_full_first:
        if e.first not in first_map:
            first_map[e.first] = set()
        first_map[e.first].add(e)

    # Construct a new director for each name partition
    directors_with_full_first_name = []
    for first in first_map:
        entries = first_map[first]
        new_director = create_director_from_entries(entries, firm_map)
        directors_with_full_first_name.append(new_director)

    # If there are entries with first initials only, they are bundled as one director
    directors_with_only_first_initial = []
    if len(entries_without_full_first) > 0:
        # If there is no ambiguity, match the entries to the newly created director
        if len(directors_with_full_first_name) == 1:
            director = directors_with_full_first_name[0]
            for e in entries_without_full_first:
                director.associate_with_entry(e)
                firm = firm_map[e.firm_id]
                director.add_firm(firm)
                firm.add_director(director)
        # Otherwise, construct a new director with first name an initial
        else:
            new_director = create_director_from_entries(entries_without_full_first, firm_map)
            directors_with_only_first_initial.append(new_director)
    log_writer.write_directors_to_file(log_writer.LIST_NO_MIDDLE_FIRST_FULL, directors_with_full_first_name)
    log_writer.write_directors_to_file(log_writer.LIST_NO_MIDDLE_FIRST_INITIAL, directors_with_only_first_initial)
    return directors_with_full_first_name + directors_with_only_first_initial


def get_directors_with_middle(entries, firm_map, log_writer):
    """Process a set of entries with a middle name. 
    
    Entries are clustered into sets sharing a common First Initial and
    Middle Initial. Thus no two entries in different sets can be matched. 
    These sets are partitioned into singletons and non-singletons. Singleton 
    sets contain a single entry defining a Director. Non-singleton sets are
    processed by function
    `get_directors_from_non_singleton_set_with_first_and_middle`.
    
    :param log_writer: log writer
    :param entries: A set of entries, where each entry has a common First Initial, Last Name, and
        Jr Status. Furthermore, each entry has a Middle Name, either full or initialed.
    :param firm_map: Mapping from firm_id to Firm object
    :return: A list of directors resulting from the entries. Each Director in the returned list
        will have the same First Initial, Last Name, and Jr Status, and a Middle Name or Initial
    """
    # Construct Mapping from (first init, middle init) to set of satisfying entries
    mapping = {}
    for e in entries:
        if (e.first_init, e.middle_init) not in mapping:
            mapping[(e.first_init, e.middle_init)] = set()
        mapping[(e.first_init, e.middle_init)].add(e)

    # Filter singletons and non-singletons
    singletons = {}
    non_singletons = {}
    for k in mapping:
        s = mapping[k]
        if len(s) == 1:
            singletons[k] = s
        else:
            non_singletons[k] = s

    directors_from_singleton_sets = []

    # Each singleton contains an entry referencing a unique director
    for k in singletons:
        s = singletons[k]
        entry = s.pop()
        new_director = create_director_from_entry(entry, firm_map)
        directors_from_singleton_sets.append(new_director)

    # Non-singletons require more processing
    directors_from_non_singleton_sets = []
    for k in non_singletons:
        s = non_singletons[k]
        directors_from_non_singleton_sets += get_directors_from_non_singleton_set_with_first_and_middle(s, firm_map, log_writer)
    log_writer.write_directors_to_file(log_writer.LIST_MIDDLE_SINGLETONS, directors_from_singleton_sets)
    log_writer.write_directors_to_file(log_writer.LIST_MIDDLE_NON_SINGLETONS, directors_from_non_singleton_sets)
    return directors_from_singleton_sets + directors_from_non_singleton_sets


def get_directors_from_non_singleton_set_with_first_and_middle(entries, firm_map, log_writer):
    """Process a non-singleton set of entries with a common First Initial, Middle Initial, Last Name, and Jr Status.
    
    A relation set is constructed from the entries. If the relation set is transitive, the relation is an
    equivalence relation on the entries, and each equivalence class corresponds to a definable director. If the
    relation is not transitive, the entries are processed by function get_directors_from_intransitive_set.
    
    :param log_writer: log writer
    :param entries: A set of entries S, where each entry has a common First Initial, Middle Initial (not void),
        Last Name, and Jr Status. Furthermore, |S| > 1.
    :param firm_map: Mapping from firm_id to Firm object.
    :return: A list of directors resulting from the entries. Each Director in the returned list will have the same
        First Initial, Middle Initial, Last Name, and Jr Status.
    """
    directors_from_transitive_sets = []
    directors_from_intransitive_sets = []
    relation_set = get_relation_set(entries)
    if check_transitive(relation_set):
        equivalence_classes = get_equivalence_classes(relation_set)
        for eq_class in equivalence_classes.values():
            new_director = create_director_from_entries(eq_class, firm_map)
            directors_from_transitive_sets.append(new_director)
    else:
        directors_from_intransitive_sets += get_directors_from_intransitive_set(entries, firm_map, log_writer)
    log_writer.write_directors_to_file(log_writer.LIST_MIDDLE_NON_SINGLETONS_UNAMBIGUOUS, directors_from_transitive_sets)
    log_writer.write_directors_to_file(log_writer.LIST_MIDDLE_NON_SINGLETONS_AMBIGUOUS, directors_from_intransitive_sets)
    return directors_from_transitive_sets + directors_from_intransitive_sets


def get_directors_from_intransitive_set(entries, firm_map, log_writer):
    """Process a set of entries with a common First Initial, Middle Initial, Last Name, and Jr Status, where the set
    is not transitive under the name equivalence relation. 
        
    The set is partitioned into two sets: entries with both
    First Name and Middle Name being initials, and entries with at least one of First Name and Middle Name being
    full. If there are no dual initial entries, the non-transitivity is a result of ambiguous cases like
            { John Jacob, John J, J John }
    So the entries are processed by the function get_directors_from_ambiguous_entries.
    If there is a dual initial entry, this entry will be matched ambiguously with the other entries, so it is
    assumed to be a distinct Director. The non-dual initial entries are then checked for transitivity. If
    transitive, Directors are created from the equivalence classes. If not, they are ambiguous and processed by
    the function get_directors_from_ambiguous_entries.

    :param log_writer: log writer
    :param entries: A set of entries where each entry has a common First Initial, Middle Initial (not void),
        Last Name, and Jr Status. The set of entries is not transitive under the name equivalence relation.
    :param firm_map: Mapping from firm_id to Firm object.
    :return: A list of directors resulting from the entries. Each Director in the returned list will have the same
        First Initial, Middle Initial, Last Name, and Jr Status.
    """
    # remove dual initial entries
    entries_with_dual_initials = set()
    entries_wo_dual_initials = set()
    for e in entries:
        if e.is_first_init and e.is_middle_init:
            entries_with_dual_initials.add(e)
        else:
            entries_wo_dual_initials.add(e)

    # If there are entries with dual initials, they are ambiguously matched to other entries, so construct a director.
    if len(entries_with_dual_initials) > 0:
        director_from_dual_initials = []
        new_director = create_director_from_entries(entries_with_dual_initials, firm_map)
        director_from_dual_initials.append(new_director)

        # Process entries without dual initials using the check transitivity method.
        relation_set = get_relation_set(entries_wo_dual_initials)
        # If transitive, construct directors
        if check_transitive(relation_set):
            directors_from_resulting_transitive_set = []
            equivalence_classes = get_equivalence_classes(relation_set)
            for eq_class in equivalence_classes.values():
                new_director = create_director_from_entries(eq_class, firm_map)
                directors_from_resulting_transitive_set.append(new_director)
            log_writer.write_directors_to_file(log_writer.LIST_AMBIGUOUS_DUAL_INITIAL_CULPRIT, director_from_dual_initials)
            log_writer.write_directors_to_file(log_writer.LIST_UNAMBIGUOUS_WITH_DUAL_INITIAL_REMOVED, directors_from_resulting_transitive_set)
            return director_from_dual_initials + directors_from_resulting_transitive_set
        # If not transitive, process the ambiguous entries
        else:
            directors_from_ambiguous_entries = get_directors_from_ambiguous_entries(entries_wo_dual_initials, firm_map, log_writer)
            log_writer.write_directors_to_file(log_writer.LIST_AMBIGUOUS_DUAL_INITIAL_NON_CULPRIT, director_from_dual_initials)
            log_writer.write_directors_to_file(log_writer.LIST_TRULY_AMBIGUOUS, directors_from_ambiguous_entries)
            return director_from_dual_initials + directors_from_ambiguous_entries

    # If there are no entries with dual initials, the non-transitivity is a result of ambiguous first and middle names
    # So process ambiguous entries
    else:
        directors_from_ambiguous_entries = get_directors_from_ambiguous_entries(entries_wo_dual_initials, firm_map, log_writer)
        log_writer.write_directors_to_file(log_writer.LIST_TRULY_AMBIGUOUS, directors_from_ambiguous_entries)
        return directors_from_ambiguous_entries


def get_directors_from_ambiguous_entries(entries, firm_map, log_writer):
    """Process a set of entries with a common First Initial, Middle Initial, Last Name, and Jr Status, where the set
    is not transitive under the name equivalence relation, and has no dual initial entries. 
    
    A director is constructed for each distinct Full Name in the entries.

    :param log_writer: log writer
    :param entries: A set of entries with a common First Initial, Middle Initial, Last Name, and Jr Status. The set is
        not transitive under the name equivalence relation, and does not contain dual initial entries.
    :param firm_map: Mapping from firm_id to Firm object.
    :return: A list of directors resulting from the entries. A director is created for each distinct Full Name
    """
    full_name_map = {}
    for e in entries:
        if e.full_name not in full_name_map:
            full_name_map[e.full_name] = set()
        full_name_map[e.full_name].add(e)
    new_directors = []
    for k in full_name_map:
        s = full_name_map[k]
        new_director = create_director_from_entries(s, firm_map)
        new_directors.append(new_director)
    return new_directors


####################
# Entry Partitions #
####################

def get_entries_with_and_without_middle(entries):
    entries_with_middle = set()
    entries_without_middle = set()
    for e in entries:
        if e.middle:
            entries_with_middle.add(e)
        else:
            entries_without_middle.add(e)
    return entries_with_middle, entries_without_middle

def get_entries_with_and_without_full_first(entries):
    entries_with_full_first = set()
    entries_without_full_first = set()
    for e in entries:
        if e.is_first_init:
            entries_without_full_first.add(e)
        else:
            entries_with_full_first.add(e)
    return entries_with_full_first, entries_without_full_first

#####################
# Director Creation #
#####################

def create_director_from_entry(e, firm_map):
    firm = firm_map[e.firm_id]
    director = Director(*e.get_director_constructor())
    director.add_firm(firm)
    firm.add_director(director)
    return director

def create_director_from_entries(entries, firm_map):
    director = create_director_from_entry(entries.pop(), firm_map)
    for e in entries:
        director.associate_with_entry(e)
        firm = firm_map[e.firm_id]
        director.add_firm(firm)
        firm.add_director(director)
    return director

########################
#  Relation Functions  #
########################

def get_relation_set(entries):
    relation_set = set()
    for e1 in entries:
        for e2 in entries:
            if compare_entries_with_first_and_middle_init_and_same_last_and_suffix(e1, e2):
                relation_set.add((e1, e2))
    return relation_set

def check_transitive(relation_set):
    for e1, e2 in relation_set:
        for e3, e4 in relation_set:
            if e2 == e3:
                if (e1, e4) not in relation_set:
                    return False
    return True

def get_equivalence_classes(relation_set):
    classes = {}  # map from representative entry to eq class, a set
    for e1, e2 in relation_set:
        placed = False
        for representative in classes:
            if (e1, representative) in relation_set:
                placed = True
                classes[representative].add(e1)
                classes[representative].add(e2)
        if not placed:
            classes[e1] = {e1, e2}
    return classes

#######################
#   NAME COMPARISON   #
#######################

def compare_entries_with_first_and_middle_init_and_same_last_and_suffix(e1, e2):
    return compare_first_names(e1, e2) and compare_middle_names(e1, e2)

def compare_first_names(e1, e2):
    if e1.first == e2.first:
        return True
    elif e1.is_first_init or e2.is_first_init:
        return e1.first_init == e2.first_init
    else:
        return False

def compare_middle_names(e1, e2):
    if e1.middle == e2.middle:
        return True
    elif e1.is_middle_init or e2.is_middle_init:
        return e1.middle_init == e2.middle_init
    else:
        return False

###############
#   Merging   #
###############

def merge_directors(directors_with_middle, directors_without_middle):
    """Merge directors with and without middle names. 
    
    Input lists contain directors with the same First Initial,
    Last Name, and Suffix. A mapping is constructed from Full First Name to a set of directors with
    middle names that have that first name. Then directors with full first names and without middle names are
    merged to a matching director with a middle name, if unambiguous.
    
    :param directors_with_middle: List of Directors with a middle name
    :param directors_without_middle: List of Directors without a middle name
    :return a combined list of directors, having been merged, with merged directors deleted.
    """
    unmerged_directors_without_middle = []
    mapping = {}
    for d in directors_with_middle:
        if not d.is_first_init:
            k = (d.first, d.last, d.suffix)
            if k not in mapping:
                mapping[k] = set()
            mapping[k].add(d)

    for d in directors_without_middle:
        if not d.is_first_init:
            k = (d.first, d.last, d.suffix)
            if k in mapping and len(mapping[k]) == 1:
                director_with_middle = mapping[k].pop()
                if not director_with_middle.merge(d):
                    unmerged_directors_without_middle.append(d)
            else:
                unmerged_directors_without_middle.append(d)
        else:
            unmerged_directors_without_middle.append(d)

    return directors_with_middle + unmerged_directors_without_middle

##################
#   Un-linking   #
##################

def unlink_directors_with_duplicate_firms(directors, firm_map, log_writer):
    directors_to_return = []
    directors_constructed = []
    for d in directors:
        if d.flagged_for_duplicate_entry:
            d.remove_from_firms()
            entries = d.entries
            # Partition entries by full name, note that no two entries with same full name will have same firm
            # THIS IS AN ASSUMPTION: Possible room for errors
            mapping = {}
            for e in entries:
                if e.full_name not in mapping:
                    mapping[e.full_name] = set()
                mapping[e.full_name].add(e)
            for s in mapping.values():
                new_director = create_director_from_entries(s, firm_map)
                directors_to_return.append(new_director)
                directors_constructed.append(new_director)
        else:
            directors_to_return.append(d)
    log_writer.write_directors_to_file(log_writer.LIST_DIRECTORS_CONSTRUCTED_FROM_DUPLICATE_FIRM_ISSUE, directors_constructed)
    return directors_to_return
