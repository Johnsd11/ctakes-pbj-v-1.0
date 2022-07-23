from cassis import *
import pbj_sender

sender = pbj_sender.PBJSender('queue/test')


class XmiToCasHandler:

    # default constructor
    def __init__(self):
        with open('resources/TypeSystem.xml', 'rb') as f:
            self.typesystem = load_typesystem(f)

    def xmi_to_cas(self,xmi):
        # tests/test_files/xmi/GenSurg_UmbilicalHernia_1.xmi
        with open(xmi, 'rb') as f:
            # casVar gets a CAS from an XMI
            casVar = load_cas_from_xmi(f, typesystem=self.typesystem)
        return casVar
