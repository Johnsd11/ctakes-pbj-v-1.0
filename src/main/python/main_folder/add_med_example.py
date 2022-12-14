from cassis import *

import add_modifier as am
import create_type as ct
from ctakes_types import *
from pbj_util import TypeSystemAccessor

# Load the type system.
typesystem = TypeSystemAccessor().get_type_system()

# Create the Cas.
cas = Cas(typesystem)

text = "Patient takes 40 mg Aspirin per day"
cas.sofa_string = text

# Create a MedicationMention.
med_type = ct.create_type(cas, MedicationMention, 20, 27)

# Add a strength Modifier to the MedicationMention.  Right now we need to specify the attribute name.
am.add_modifier(cas, med_type, MedicationStrengthModifier, 14, 19, "medicationStrength")

# Run through the cas fetching medications and their strengths.
for med in cas.select(MedicationMention):
    print(med.get_covered_text())
    med_str = med.get("medicationStrength")
    print(med_str.get_covered_text())
