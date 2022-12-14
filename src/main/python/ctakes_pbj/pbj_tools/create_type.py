def create_type(cas, type_name, begin, end):
    # Create and add a Type
    type_type = cas.typesystem.get_type(type_name)
    return add_type(cas, type_type, begin, end)


def add_type(cas, type_type, begin, end):
    #  Add a type.  If a known type is repeatedly added then it is faster to get the type from the type system once
    #  and call this function repeatedly with the given type.
    ts_type = type_type(begin=begin, end=end)
    cas.add(ts_type)
    return ts_type