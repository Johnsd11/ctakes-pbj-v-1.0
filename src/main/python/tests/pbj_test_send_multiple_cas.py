# 1. Read an example XMI file,
# 2. Send.

import pbj_sender
from cassis import *
# These are the lines that ignore the typesystem errors
import warnings

warnings.filterwarnings("ignore")

# loading the TypeSystem for the process specified by the user
with open('resources/TypeSystem.xml', 'rb') as f:
    typesystem = load_typesystem(f)

# Opening the xmi file provided by user and converting it into a cas
with open('tests/test_files/xmi/Peds_FebrileSez_1.xmi', 'rb') as f:
    cas1 = load_cas_from_xmi(f, typesystem=typesystem)

with open('tests/test_files/xmi/Peds_Dysphagia_1.xmi', 'rb') as f:
    cas2 = load_cas_from_xmi(f, typesystem=typesystem)

#
pbj_sender1 = pbj_sender.PBJSender('queue/test')
pbj_sender2 = pbj_sender.PBJSender('queue/test')

pbj_sender1.sendJCas(cas1)
pbj_sender2.sendJCas(cas2)
print("sent")
