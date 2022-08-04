# 1. Read an example XMI file,
# 2. Send.
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from pbj_sender import *
        from pbj_util import *
    else:
        from ..pbj_sender import *
        from ..pbj_util import *
from cassis import *
# These are the lines that ignore the typesystem errors
import warnings

warnings.filterwarnings("ignore")

# loading the TypeSystem for the process specified by the user
with open(CTAKES_TYPE_SYSTEM, 'rb') as f:
    typesystem = load_typesystem(f)

# Opening the xmi file provided by user and converting it into a cas for
with open("../../../resources/xmi_dir/OBGYN_HysterectomyAndBSO_1.xmi", 'rb') as f:
    cas = load_cas_from_xmi(f, typesystem=typesystem)

# explain whats going on here
pbj_sender = PBJSender('queue/test')
pbj_sender.send_jcas(cas)
print("sent")
