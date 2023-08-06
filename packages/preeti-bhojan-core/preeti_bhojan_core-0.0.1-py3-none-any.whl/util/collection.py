def is_distinct(list_):
    """
    Does `list_` only contain distinct/unique elements?
    :param list_: the list to test
    :return: true if list_ contains only unique elements false otherwise
    """
    return len(set(list_)) == len(list_)


def is_subset(list_, sub_list):
    """
    Is sublist a subset of the given list?
    :param list_: the list
    :param sub_list: the sublist
    :return: true if the sublist a subset of list false otherwise.
    """
    return set(sub_list).issubset(set(list_))


def consists_of_same_element(list_):
    """
    Checks if a list consists of single element like [5, 5, 5]
    :param list_: list to check
    :return: bool
    """
    return len(set(list_)) == 1
