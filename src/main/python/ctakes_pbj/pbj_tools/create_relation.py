
def create_relation(types, category, source, target):
    tlink = types()
    tlink.category = category
    tlink.arg1 = source
    tlink.arg2 = target
    return tlink
