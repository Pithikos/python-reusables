def diff_lists(l1, l2):
    if len(l1)>len(l2):
        return [i for i in l1 if not i in l2]
    else:
        return [i for i in l2 if not i in l1]
