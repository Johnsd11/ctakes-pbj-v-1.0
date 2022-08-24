from main_folder.cas_to_xmi_handler import *
from main_folder.pbj_sender_v2 import PBJSender
from main_folder.xmi_to_cas_handler import *

# if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         from os import path
#         sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#         from cas_to_xmi_handler import *
#         from xmi_to_cas_handler import *
#         from pbj_sender_v2 import *
#     else:
#         from ..cas_to_xmi_handler import *
#         from ..xmi_to_cas_handler import *
#         from ..pbj_sender_v2 import *


# TAKES CAS -> XMI

cas_to_xmi_handler = CasToXmiHandler()
xmi_to_cas_handler = XmiToCasHandler()
sender = PBJSender('queue/test')

# Test Setup
# first creates a cas with an example XMI
cas = xmi_to_cas_handler.xmi_to_cas("../../../resources/xmi_dir/OBGYN_HysterectomyAndBSO_1.xmi")

# Normally User code would do something with the cas

sender.process(cas, CTAKES_TYPE_SYSTEM)

# Then converts that cas back to XMI
xmiText = cas_to_xmi_handler.cas_to_xmi(cas)

# send the xmi to receiver
# sender.send(xmiText)
print(xmiText)




