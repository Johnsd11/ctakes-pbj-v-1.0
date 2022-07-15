
from ctakes_types import *
from cassis import *
from cassis.typesystem import TYPE_NAME_FS_ARRAY
import pbj_util


# Load the typesystem
type_system_accessor = pbj_util.TypeSystemAccessor()
type_system_accessor.load_type_system()
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

# Create a MedicationStrengthModifier
strength_type = cas.typesystem.get_type(MedicationStrengthModifier)
strength_mod = strength_type(begin=14, end=19)
cas.add(strength_mod)

# Create a MedicationStrength (Attribute)
strength_attr_type = cas.typesystem.get_type(MedicationStrength)
strength_attr = strength_attr_type()
cas.add(strength_attr)

# Create an FSArray of modifiers (specifically strength modifiers)
strength_mods = FSArray(elements=[strength_mod])
strength_attr.mentions = strength_mods

# Set Attribute in Medication
med_type.medicationStrength = strength_attr

cas.add(strength_mods)


for med_attr in cas.select(MedicationStrength):
    fs_array = med_attr.get("mentions")
    elements = fs_array.elements
    for element in elements:
        print(element.get_covered_text())
