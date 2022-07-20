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

# Opening the xmi file provided by user and converting it into a cas for
with open('tests/test_files/xmi/Peds_FebrileSez_1.xmi', 'rb') as f:
    cas = load_cas_from_xmi(f, typesystem=typesystem)

# explain whats going on here
pbj_sender = pbj_sender.PBJSender('queue/test')
pbj_sender.send_jcas(cas)
print("sent")
