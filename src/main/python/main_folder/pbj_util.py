import cassis

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 61616
DEFAULT_USER = 'guest'
DEFAULT_PASS = 'guest'
CTAKES_TYPE_SYSTEM_TESTS = "../../../../../../ctakes-type-system/src/main/resources/org/apache/ctakes/typesystem/types/TypeSystem.xml"
CTAKES_TYPE_SYSTEM = "../../../../../ctakes-type-system/src/main/resources/org/apache/ctakes/typesystem/types/TypeSystem.xml"
# Idk what I'm doing here exactly
#CTAKES_TYPE_SYSTEM = "ctakes-type-system/src/main/resources/org/apache/ctakes/typesystem/types/TypeSystem.xml"
STOP_MESSAGE = "Apache cTAKES PBJ Stop Message."
XMI_INDICATOR = "xmlns:xmi"


class TypeSystemAccessor:

    def __init__(self, type_system_file=CTAKES_TYPE_SYSTEM):
        self.typesystem = None
        self.type_system_file = type_system_file

    def load_type_system(self):
        if self.typesystem is None:
            with open(self.type_system_file, 'rb') as f:
                self.typesystem = cassis.load_typesystem(f)

    def get_type_system(self):
        self.load_type_system()
        return self.typesystem
