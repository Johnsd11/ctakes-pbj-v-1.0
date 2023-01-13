import cassis
CTAKES_TYPE_SYSTEM_TESTS = "../../../../../../ctakes-type-system/src/main/resources/org/apache/ctakes/typesystem/types/TypeSystem.xml"
CTAKES_TYPE_SYSTEM = "resources/org/apache/ctakes/typesystem/types/TypeSystem.xml"
XMI_INDICATOR = "xmlns:xmi"


class TypeSystemLoader:

    def __init__(self, type_system_file=CTAKES_TYPE_SYSTEM):
        self.typesystem = None
        self.type_system_file = type_system_file

    def load_type_system(self):
        print("in load typesystem")
        if self.typesystem is None:
            with open(self.type_system_file, 'rb') as f:
                self.typesystem = cassis.load_typesystem(f)

    def get_type_system(self):
        self.load_type_system()
        return self.typesystem
