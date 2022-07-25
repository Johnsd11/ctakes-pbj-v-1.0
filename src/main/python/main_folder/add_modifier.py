def add_modifier(cas, event_mention, mod_name, begin, end, property_name=""):
    # Create and add a Modifier
    mod_type = cas.typesystem.get_type(mod_name)
    mod = mod_type(begin=begin, end=end)

    if property_name == "":
        # Configure attr to have a lower case first letter
        mod_array = mod_name.split(".")
        lowercase_mod = mod_array[-1][0].lower() + mod_array[-1][1:]
        # Set Attribute in EventMention
        event_mention.set(lowercase_mod, mod)
    else:
        event_mention.set(property_name, mod)

    cas.add(mod)
