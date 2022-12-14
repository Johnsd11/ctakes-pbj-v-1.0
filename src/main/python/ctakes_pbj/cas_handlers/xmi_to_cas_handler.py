from cassis import *
from ctakes_pbj import pbj_sender
from ctakes_pbj.pbj_util import *
from pathlib import *
sender = pbj_sender.PBJSender('queue/test')


class XmiToCasHandler:

    # default constructor
    def __init__(self):
        # get current path then go back until you find "ctakes-pb"
        # get parent of ctakes-pbj and add in CTAKES_TYPE_SYSTEM
        current_dir = Path.cwd()
        while current_dir.stem != "ctakes-pbj":
            current_dir = current_dir.parent

        with open(str(current_dir.parent) + "/" + CTAKES_TYPE_SYSTEM, 'rb') as f:
            self.typesystem = load_typesystem(f)

    def xmi_to_cas(self, xmi):
        # tests/test_files/xmi/GenSurg_UmbilicalHernia_1.xmi.xmi
        with open(xmi, 'rb') as f:
            # casVar gets a CAS from an XMI
            casVar = load_cas_from_xmi(f, typesystem=self.typesystem)
        return casVar
