import cassis
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

    # def xmi_only(self):


    
    # UpperCase class name: XmiToCasHandler
    # We don't want to load the typesystem for every new cas as it doesn't change.
    # So, set the typesystem in an __init__ constructor so you can call xmi_handler = XmiToCasHandler('resources/TypeSystem.xml')
    # After that I think that this is 100% correct.  A user could call xmi_handler.xmi_to_cas(xmi).
    # More to the point, next week we can make a child class that extends this with a generic "print" of the xmi.
    # Much later we will extend for various ML projects.
