NE_TYPE_ID_UNKNOWN = 0
NE_TYPE_ID_DRUG = 1
NE_TYPE_ID_DISORDER = 2
NE_TYPE_ID_FINDING = 3
NE_TYPE_ID_PROCEDURE = 5
NE_TYPE_ID_ANATOMICAL_SITE = 6
NE_TYPE_ID_CLINICAL_ATTRIBUTE = 7
NE_TYPE_ID_DEVICE = 8
NE_TYPE_ID_LAB = 9
NE_TYPE_ID_PHENOMENA = 10
NE_TYPE_ID_SUBJECT_MODIFIER = 1001
NE_TYPE_ID_PERSON_TITLE = 1002
NE_TYPE_ID_GENERIC_EVENT = 1003
NE_TYPE_ID_GENERIC_ENTITY = 1004
NE_TYPE_ID_TIME_MENTION = 1005
NE_TYPE_ID_GENERIC_MODIFIER = 1006
NE_TYPE_ID_LAB_VALUE_MODIFIER = 1007
NE_DISCOVERY_TECH_DICT_LOOKUP = 1
NE_DISCOVERY_TECH_GOLD_ANNOTATION = 2
NE_DISCOVERY_TECH_EXPLICIT_AE = 3
NE_POLARITY_NEGATION_ABSENT = 1
NE_POLARITY_NEGATION_PRESENT = -1
NE_UNCERTAINTY_PRESENT = 1
NE_UNCERTAINTY_ABSENT = 0
NE_HISTORY_OF_PRESENT = 1
NE_HISTORY_OF_ABSENT = 0
NE_GENERIC_TRUE = True
NE_GENERIC_FALSE = False
NE_CONDITIONAL_TRUE = True
NE_CONDITIONAL_FALSE = False
NE_CERTAINTY_POSITIVE = NE_POLARITY_NEGATION_ABSENT  # // TO BE DEPRECATED
NE_CERTAINTY_NEGATED = NE_POLARITY_NEGATION_PRESENT  # // TO BE DEPRECATED
NE_DIAG_STATUS_CONFIRMED = 0  # // TO BE DEPRECATED
NE_DIAG_STATUS_HISTORY_OF = 1  # // TO BE DEPRECATED
NE_DIAG_STATUS_FAM_HISTORY_OF = 2  # // TO BE DEPRECATED
NE_DIAG_STATUS_PROBABLE = 3  # // TO BE DEPRECATED
MODIFIER_TYPE_ID_UNKNOWN = 0
MODIFIER_TYPE_ID_COURSE_CLASS = 1
MODIFIER_TYPE_ID_SEVERITY_CLASS = 2
MODIFIER_TYPE_ID_LAB_INTERPRETATION_INDICATOR = 3
# ATTR_PROCEDURE_DEVICE -- any
# ATTR_PROCEDURE_METHOD -- any
# ATTR_LAB_VALUE_NUMBER -- any
# ATTR_LAB_VALUE_UNIT -- any
# ATTR_LAB_REFERENCE_RANGE -- any
ATTR_SEVERITY_SEVERE = "severe"
ATTR_SEVERITY_MODERATE = "moderate"
ATTR_SEVERITY_SLIGHT = "slight"
ATTR_SEVERITY_UNMARKED = "unmarked"
ATTR_BODYSIDE_LEFT = "left"
ATTR_BODYSIDE_RIGHT = "right"
ATTR_BODYSIDE_BILATERAL = "bilateral"
ATTR_BODYSIDE_UNMARKED = "unmarked"
ATTR_BODYLATERALITY_SUPERIOR = "superior"  # // Attribute name may change
ATTR_BODYLATERALITY_INFERIOR = "inferior"  # // Attribute name may change
ATTR_BODYLATERALITY_DISTAL = "distal"  # // Attribute name may change
ATTR_BODYLATERALITY_PROXIMAL = "proximal"  # // Attribute name may change
ATTR_BODYLATERALITY_MEDIAL = "medial"  # // Attribute name may change
ATTR_BODYLATERALITY_LATERAL = "lateral"  # // Attribute name may change
ATTR_BODYLATERALITY_DORSAL = "dorsal"  # // Attribute name may change
ATTR_BODYLATERALITY_VENTRAL = "ventral"  # // Attribute name may change
ATTR_BODYLATERALITY_UNMARKED = "unmarked"  # // Attribute name may change
ATTR_HISTORYOF_INDICATOR_PRESENT = "historyOf_present"
ATTR_HISTORYOF_INDICATOR_ABSENT = "historyOf_absent"
ATTR_SUBJECT_PATIENT = "patient"
ATTR_SUBJECT_FAMILY_MEMBER = "family_member"
ATTR_SUBJECT_DONOR_FAMILY_MEMBER = "donor_family_member"
ATTR_SUBJECT_DONOR_OTHER = "donor_other"
ATTR_SUBJECT_OTHER = "other"
ATTR_LAB_DELTAFLAG_CHANGEUP = "change_up"
ATTR_LAB_DELTAFLAG_CHANGEDOWN = "change_down"
ATTR_LAB_DELTAFLAG_NOCHANGE = "no_change"
ATTR_LAB_ABNORMAL_TRUE = "abnormal"
ATTR_LAB_ABNORMAL_VERYTRUE = "very_abnormal"
ATTR_LAB_ORDINAL_RESISTANT = "resistant"
ATTR_LAB_ORDINAL_POSITIVE = "positive"
ATTR_LAB_ORDINAL_REACTIVE = "reactive"
ATTR_LAB_ORDINAL_INTERMEDIATERESISTANCE = "intermediate_resistance"
ATTR_LAB_ORDINAL_INTERMEDIATE = "intermediate"
ATTR_LAB_ORDINAL_NEGATIVE = "negative"
ATTR_LAB_ORDINAL_NOTDETECTED = "not_detected"
ATTR_LAB_ORDINAL_DETECTED = "detected"
ATTR_LAB_ORDINAL_WEAKLY_REACTIVE = "weakly_reactive"
ATTR_LAB_ORDINAL_MODERATELYSUSCEPTIBLE = "moderately_susceptible"
ATTR_LAB_ORDINAL_VERYSUSCEPTIBLE = "very_susceptible"
ATTR_LAB_ORDINAL_SUSCEPTIBLE = "susceptible"
ATTR_LAB_ORDINAL_1ORMORE = "1+"
ATTR_LAB_ORDINAL_2ORMORE = "2+"
ATTR_LAB_ORDINAL_3ORMORE = "3+"
ATTR_LAB_ORDINAL_4ORMORE = "4+"
ATTR_LAB_ORDINAL_SMALL = "small"
ATTR_LAB_ORDINAL_TRACE = "trace"
ATTR_LAB_ORDINAL_NORMAL = "normal"
ATTR_LAB_ORDINAL_NO_OR_NA_RANGE = "no_range_or_normal_range_n/a"
ATTR_LAB_ORDINAL_ANTICOMPLEMENTARYPRESENT = "anti_complementary_substance_present"
ATTR_LAB_ORDINAL_CYTOTOXICPRESENT = "cytotoxic_substance_present"
ATTR_LAB_ORDINAL_QUALITYCONTROLFAIL = "quality_control_failure"
ATTR_LAB_ESTIMATED_FLAG_TRUE = True
ATTR_LAB_ESTIMATED_FLAG_FALSE = False
ATTR_MEDICATION_DOSAGE_1 = 1
ATTR_MEDICATION_DOSAGE_2 = 2
ATTR_MEDICATION_DOSAGE_3 = 3
ATTR_MEDICATION_DOSAGE_4 = 4
ATTR_MEDICATION_DOSAGE_5 = 5
ATTR_MEDICATION_DOSAGE_UNDETERMINED = "undetermined"
ATTR_MEDICATION_DOSAGE_OTHER = "other"
ATTR_MEDICATION_ROUTE_TOPICAL = "topical"
ATTR_MEDICATION_ROUTE_ENTERAL_ORAL = "oral"
ATTR_MEDICATION_ROUTE_ENTERAL_GASTRIC = "gastric"
ATTR_MEDICATION_ROUTE_ENTERAL_RECTAL = "rectal"
ATTR_MEDICATION_ROUTE_PARENTERAL_INTRAVENOUS = "intravenous"
ATTR_MEDICATION_ROUTE_PARENTERAL_INTRAARTERIAL = "intra-arterial"
ATTR_MEDICATION_ROUTE_PARENTERAL_INTRAMUSCULAR = "intramuscular"
ATTR_MEDICATION_ROUTE_PARENTERAL_INTRACARDIAC = "intracardiac"
ATTR_MEDICATION_ROUTE_PARENTERAL_SUBCUTANEOUS = "subcutaneous"
ATTR_MEDICATION_ROUTE_PARENTERAL_INTRATHECAL = "intrathecal"
ATTR_MEDICATION_ROUTE_PARENTERAL_INTRAPERIOTONEAL = "intraperiotoneal"
ATTR_MEDICATION_ROUTE_PARENTERAL_TRANSDERMAL = "transdermal"
ATTR_MEDICATION_ROUTE_PARENTERAL_TRANSMUCOSAL = "transmucosal"
ATTR_MEDICATION_ROUTE_OTHER = "other"
ATTR_MEDICATION_ROUTE_UNDETERMINED = "undetermined"
ATTR_MEDICATION_FORM_AEROSOL = "aerosol"
ATTR_MEDICATION_FORM_CAPSULE = "capsule"
ATTR_MEDICATION_FORM_CREAM = "cream"
ATTR_MEDICATION_FORM_ELIXIR = "elixir"
ATTR_MEDICATION_FORM_EMULSION = "emulsion"
ATTR_MEDICATION_FORM_ENEMA = "enema"
ATTR_MEDICATION_FORM_GEL = "gel"
ATTR_MEDICATION_FORM_IMPLANT = "implant"
ATTR_MEDICATION_FORM_INHALANT = "inhalant"
ATTR_MEDICATION_FORM_INJECTION = "injection"
ATTR_MEDICATION_FORM_LIQUID = "liquid"
ATTR_MEDICATION_FORM_LOTION = "lotion"
ATTR_MEDICATION_FORM_LOZENGE = "lozenge"
ATTR_MEDICATION_FORM_OINTMENT = "ointment"
ATTR_MEDICATION_FORM_PATCH = "patch"
ATTR_MEDICATION_FORM_PELLET = "pellet"
ATTR_MEDICATION_FORM_PILL = "pill"
ATTR_MEDICATION_FORM_POWDER = "powder"
ATTR_MEDICATION_FORM_SHAMPOO = "shampoo"
ATTR_MEDICATION_FORM_SOAP = "soap"
ATTR_MEDICATION_FORM_SOLUTION = "solution"
ATTR_MEDICATION_FORM_SPRAY = "spray"
ATTR_MEDICATION_FORM_SUPPOSITORY = "suppository"
ATTR_MEDICATION_FORM_SYRUP = "syrup"
ATTR_MEDICATION_FORM_TABLET = "tablet"
ATTR_MEDICATION_FORM_OTHER = "other"
ATTR_MEDICATION_STATUSCHANGE_START = "start"
ATTR_MEDICATION_STATUSCHANGE_STOP = "stop"
ATTR_MEDICATION_STATUSCHANGE_INCREASE = "increase"
ATTR_MEDICATION_STATUSCHANGE_DECREASE = "decrease"
ATTR_MEDICATION_STATUSCHANGE_NOCHANGE = "noChange"
ATTR_MEDICATION_ALLERGY_INDICATOR_PRESENT = "allergy_present"
ATTR_MEDICATION_ALLERGY_INDICATOR_ABSENT = "allergy_absent"

#    // ATTR_MEDICATION_STRENGTH is any number/unit pair
#    // ATTR_MEDICATION_DURATION is any
#    // ATTR_MEDICATION_FREQUENCY is any number/unit pair

REL_DISCOVERY_TECH_GOLD_ANNOTATION = 1

MED_STATUS_CHANGE_START = ATTR_MEDICATION_STATUSCHANGE_START  # // TO BE DEPRECATED
MED_STATUS_CHANGE_STOP = ATTR_MEDICATION_STATUSCHANGE_STOP  # // TO BE DEPRECATED
MED_STATUS_CHANGE_INCREASEFROM = "increasefrom"  # // TO BE DEPRECATED
MED_STATUS_CHANGE_DECREASEFROM = "decreasefrom"  # // TO BE DEPRECATED
MED_STATUS_CHANGE_INCREASE = ATTR_MEDICATION_STATUSCHANGE_INCREASE  # // TO BE DEPRECATED
MED_STATUS_CHANGE_DECREASE = ATTR_MEDICATION_STATUSCHANGE_DECREASE  # // TO BE DEPRECATED
MED_STATUS_CHANGE_NOCHANGE = ATTR_MEDICATION_STATUSCHANGE_NOCHANGE  # // TO BE DEPRECATED
MED_STATUS_CHANGE_SUM = "add"  # // TO BE DEPRECATED
MED_STATUS_CHANGE_MAX = "maximum"  # // TO BE DEPRECATED
MED_STATUS_CHANGE_OTHER = "change"  # // TO BE DEPRECATED

TIME_CLASS_DATE = "DATE"
