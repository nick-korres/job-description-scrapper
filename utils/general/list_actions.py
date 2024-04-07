def union_lists(list1,list2):
    set1 = set(list1)
    set2 = set(list2)
    result_set = set1.union(set2)
    result_list = list(result_set)
    return result_list

def intersection_lists(list1,list2):
    set1 = set(list1)
    set2 = set(list2)
    result_set = set1.intersection(set2)
    result_list = list(result_set)
    return result_list

def get_class_attributes(cls):
    return [item for item in cls.__dict__ if not callable(getattr(cls, item)) and not item.startswith('__')]