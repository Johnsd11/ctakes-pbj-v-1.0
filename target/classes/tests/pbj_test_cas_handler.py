from cas_to_xmi_handler import *
from xmi_to_cas_handler import *
from pbj_sender import *
# TAKES CAS -> XMI

cas_to_xmi_handler = CasToXmiHandler()
xmi_to_cas_handler = XmiToCasHandler()
sender = PBJSender('queue/test')

# Test Setup
# first creates a cas with an example XMI
cas = xmi_to_cas_handler.xmi_to_cas("tests/test_files/xmi/OBGYN_IUD_1.xmi")

# Normally User code would do something with the cas

sender.sendJCas(cas)

# Then converts that cas back to XMI
xmiText = cas_to_xmi_handler.cas_to_xmi(cas)

# send the xmi to receiver
# sender.send(xmiText)
print(xmiText)

#  It indicates something that can be simplified for the user in a final API.


# Current Use:
# User:
# 1.  convert cas to xmi
# 2.  send xmi

#  --> Good for a methodical developer who likes to keep track of every minute step.xmi

# ??  What about a non-developer user?

# --> Send cas
#  Internally code will convert the cas to xmi.




