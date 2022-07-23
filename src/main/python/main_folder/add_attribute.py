from cassis.typesystem import TYPE_NAME_FS_ARRAY


def add_attribute(cas, medication_event_mention, mod_name, attr_name, begin, end):

    # Create and add a Modifier
    Mod = cas.typesystem.get_type(mod_name)
    mod = Mod(begin=begin, end=end)
    cas.add(mod)

    # Create and add an attribute
    Attr = cas.typesystem.get_type(attr_name)
    attr = Attr()
    cas.add(attr)

    # Create an FSArray of modifiers
    FSArray = cas.typesystem.get_type(TYPE_NAME_FS_ARRAY)
    mods = FSArray(elements=[mod])
    cas.add(mods)
    attr.mentions = mods

    # Configure attr to have a lower case first letter
    attr_array = attr_name.split(".")
    lowercase_attr = attr_array[-1][0].lower() + attr_array[-1][1:]

    # Set Attribute in Medication
    setattr(medication_event_mention, lowercase_attr, attr)

