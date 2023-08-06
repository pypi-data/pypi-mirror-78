

def return_indices(l, elems):
    
    placeholder = []
    
    for elem in elems:
        
        placeholder.append(l.index(elem))
        
    return placeholder

def get_max_value_key(d):
    
    return max(d, key=d.get)

def get_min_value_key(d):
    
    return min(d, key=d.get)

    