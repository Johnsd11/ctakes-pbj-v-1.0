import cassis

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 61616
DEFAULT_USER = 'guest'
DEFAULT_PASS = 'guest'
CTAKES_TYPE_SYSTEM = "../../../../ctakes-type-system/src/main/resources/org/apache/ctakes/typesystem/types/TypeSystem.xml"
STOP_MESSAGE = "Your Friendly neighborhood stop message. Just so that this never looks like anything that ctakes would actually read in a note."


class TypeSystemAccessor:

    def __init__(self, type_system_file=CTAKES_TYPE_SYSTEM):
        with open(type_system_file, 'rb') as f:
            self.typesystem = cassis.load_typesystem(f)

    def getTypeSystem(self):
        return self.typesystem
