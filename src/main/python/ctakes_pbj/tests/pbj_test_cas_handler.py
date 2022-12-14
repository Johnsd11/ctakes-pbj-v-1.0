from ctakes_pbj.cas_handlers.cas_to_xmi_handler import *
from ctakes_pbj.pbj_sender import PBJSender
from ctakes_pbj.cas_handlers.xmi_to_cas_handler import *


def main():
    # TAKES CAS -> XMI

    cas_to_xmi_handler = CasToXmiHandler()
    xmi_to_cas_handler = XmiToCasHandler()
    sender = PBJSender('queue/test')

    # Test Setup
    # first creates a cas with an example XMI
    cas = xmi_to_cas_handler.xmi_to_cas("../../../resources/xmi_dir/OBGYN_HysterectomyAndBSO_1.xmi")

    # Normally User code would do something with the cas

    sender.process(cas)
    sender.send_stop()

    # Then converts that cas back to XMI
    xmiText = cas_to_xmi_handler.cas_to_xmi(cas)

    # send the xmi to receiver
    # sender.send(xmiText)
    print(xmiText)


if __name__ == "__main__":
    main()





