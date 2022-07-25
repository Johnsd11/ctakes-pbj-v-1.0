from cassis import *

import add_modifier as am
import create_type as ct
import pbj_util
from ctakes_types import *

# Load the typesystem
type_system_accessor = pbj_util.TypeSystemAccessor()
type_system_accessor.load_type_system()
typesystem = type_system_accessor.get_type_system()

# Create the Cas
cas = Cas(typesystem)

text = "Patient takes 40 mg Aspirin per day"
cas.sofa_string = text

# Create a MedicationEventMention
med_type = ct.create_type(cas, MedicationMention, 20, 27)

am.add_modifier(cas, med_type, MedicationStrengthModifier, 14, 19, "medicationStrength")

for med in cas.select(MedicationMention):
    print(med.get_covered_text())
    med_str = med.get("medicationStrength")
    print(med_str.get_covered_text())
