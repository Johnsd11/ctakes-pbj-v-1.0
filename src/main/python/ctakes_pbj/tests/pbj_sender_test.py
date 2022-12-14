# 1. Read an example XMI file,
# 2. Send.
# These are the lines that ignore the typesystem errors
import warnings

from cassis import *

from ctakes_pbj.pbj_sender import PBJSender
from ctakes_pbj.pbj_util import CTAKES_TYPE_SYSTEM
from pathlib import *
# from lxml import etree
# etree.iterparse("../../../resources/xmi_dir/OBGYN_Gen_Abscess_1", tag='MyTag', encoding='iso-8859-1')

warnings.filterwarnings("ignore")


def main():

    current_dir = Path.cwd()
    while current_dir.stem != "ctakes-pbj":
        current_dir = current_dir.parent
    # loading the TypeSystem for the process specified by the user
    with open(str(current_dir.parent) + "/" + CTAKES_TYPE_SYSTEM, 'rb') as f:
        typesystem = load_typesystem(f)

    # Opening the xmi file provided by user and converting it into a cas for
    with open("../../../resources/xmi_dir/GenSurg_UmbilicalHernia_1.xmi", 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesystem)

    pbj_sender = PBJSender('queue/test')
    pbj_sender.process(cas)
    pbj_sender.send_stop()
    print("sent")


if __name__ == "__main__":
    main()


