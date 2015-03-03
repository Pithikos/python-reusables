# THIS NEES THE FUNCTION access() FROM recursion/access.py IN ORDER TO RUN


def tablefy(keystring, struct, expand_lists_to_bool=False, flatten_lists=True):
    '''
    Keystring is a string using the same syntax used in the access() function.
    The keystring will be used to give rows as a list of lists. Notice that tablefy
    will work ONLY for iterables
    keystring            - multiple keystrings separated by comma. Check access()
                           documentation for more info
    expand_lists_to_bool - convert sublists in a row into booleans. This is
                           helpful if you want more compact output.
    flatten_lists        - if we get sublists, just flatten them out. In practice
                           if we don't flatten them out then the whole sublist
                           will be used as a one cell entry
    '''
    keystrings = [expr.strip() for expr in keystring.split(',')]
    header = keystrings[:]
    cols_expanded = []

    # Get columns first
    cols =  [ access(keystring_, struct) for keystring_ in keystrings ]
    for col in cols: assert len(col)==len(cols[0])

    # Expand columns with sublists to booleans
    if expand_lists_to_bool:
        for col in cols:
            if hasattr(col[0], '__iter__'):
                bool_names = list({ item for entry in col for item in entry })
                bool_names.sort()
                cols_expanded.append([cols.index(col), bool_names])
                for i in range(len(col)):
                    col[i] = map(lambda x: x in col[i], bool_names)

    # Update header with expansions and prettify
    for i, expansion in cols_expanded:
        header[i] = expansion
    prettyfied = []
    for h in header:
        if isinstance(h, str):
            lstripped = re.search(r'([a-zA-Z].*)', h).group(1)
            rstripped = re.sub(r':.*', '', lstripped)
            prettyfied.append(rstripped)
        else:
            prettyfied.append(h)
    header = prettyfied
    
    # Make rows
    rows = [header] + zip(*cols)
    
    # Flatten sublists
    if flatten_lists:
        flattened = []
        for row in rows:
            newrow = []
            for cell in row:
                if hasattr(cell, '__iter__'):
                    newrow.extend(cell)
                else:
                    newrow.append(cell)
            flattened.append(newrow)
        rows = flattened

    return rows
