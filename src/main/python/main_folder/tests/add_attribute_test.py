from cassis import *
from cassis.typesystem import TYPE_NAME_FS_ARRAY

import main_folder.add_attribute as am
from main_folder.ctakes_types import *
from main_folder.pbj_util import *

# Load the typesystem
type_system_accessor = TypeSystemAccessor(CTAKES_TYPE_SYSTEM_TESTS)
typesystem = type_system_accessor.get_type_system()

# Create the Cas
cas = Cas(typesystem=typesystem)

text = "Patient takes 40 mg Aspirin per day"
cas.sofa_string = text
FSArray = cas.typesystem.get_type(TYPE_NAME_FS_ARRAY)

# Create a MedicationEventMention
medMention = cas.typesystem.get_type(MedicationEventMention)
med_type = medMention(begin=20, end=27)
cas.add(med_type)

am.add_attribute(cas, med_type, MedicationStrengthModifier, MedicationStrength, 14, 19)


for med_attr in cas.select(MedicationStrength):
    print("we got strength")
    fs_array = med_attr.get("mentions")
    elements = fs_array.elements
    for element in elements:
        print(element.get_covered_text())
