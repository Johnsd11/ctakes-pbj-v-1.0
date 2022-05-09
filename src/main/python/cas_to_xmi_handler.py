from cassis import *


class CasToXmiHandler:

    def cas_to_xmi(self, cas):
        # xmiVar gets an XMI from a CAS
        xmiVar = Cas.to_xmi(cas)
        return xmiVar


