# 1. Read an example XMI file,
# 2. Send.
# These are the lines that ignore the typesystem errors
import warnings

from cassis import *

from main_folder.pbj_sender_v2 import PBJSender
from main_folder.pbj_util import CTAKES_TYPE_SYSTEM

# if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         from os import path
#
#         sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#         from pbj_sender_v2 import *
#         from pbj_util import *
#     else:
#         from ..pbj_sender_v2 import *
#         from ..pbj_util import *

warnings.filterwarnings("ignore")

# loading the TypeSystem for the process specified by the user
with open(CTAKES_TYPE_SYSTEM, 'rb') as f:
    typesystem = load_typesystem(f)

# Opening the xmi file provided by user and converting it into a cas for
with open("../../../resources/xmi_dir/Peds_RoutBirthNote_1.xmi", 'rb') as f:
    cas = load_cas_from_xmi(f, typesystem=typesystem)

# explain whats going on here
pbj_sender = PBJSender('queue/test')
pbj_sender.process(cas, typesystem)
pbj_sender.send_stop()
print("sent")
