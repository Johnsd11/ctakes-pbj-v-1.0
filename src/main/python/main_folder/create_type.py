def create_type(cas, type_name, begin, end):
    # Create and add a Type
    type_type = cas.typesystem.get_type(type_name)
    ts_type = type_type(begin=begin, end=end)
    cas.add(ts_type)
    return ts_type
