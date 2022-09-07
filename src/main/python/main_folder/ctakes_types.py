#  TODO:   Turn into an enum.
#  For access you can use Ctakes.WordToken or Ctakes['WordToken'].
#  The map access style facilitates dynamic use.
#  See https://docs.python.org/3/library/enum.html

TypeSystem = "org.apache.ctakes.typesystem.types.TypeSystem"
WordToken = "org.apache.ctakes.typesystem.type.syntax.WordToken"
BaseToken = "org.apache.ctakes.typesystem.type.syntax.BaseToken"
ContractionToken = "org.apache.ctakes.typesystem.type.syntax.ContractionToken"
DocumentID = "org.apache.ctakes.typesystem.type.structured.DocumentID"
DocumentIdPrefix = "org.apache.ctakes.typesystem.type.structured.DocumentIdPrefix"
DocumentPath = "org.apache.ctakes.typesystem.type.structured.DocumentPath"
Lemma = "org.apache.ctakes.typesystem.type.syntax.Lemma"
NewlineToken = "org.apache.ctakes.typesystem.type.syntax.NewlineToken"
NumToken = "org.apache.ctakes.typesystem.type.syntax.NumToken"
OntologyConcept = "org.apache.ctakes.typesystem.type.refsem.OntologyConcept"
PunctuationToken = "org.apache.ctakes.typesystem.type.syntax.PunctuationToken"
Segment = "org.apache.ctakes.typesystem.type.textspan.Segment"
Sentence = "org.apache.ctakes.typesystem.type.textspan.Sentence"
SymbolToken = "org.apache.ctakes.typesystem.type.syntax.SymbolToken"
UmlsConcept = "org.apache.ctakes.typesystem.type.refsem.UmlsConcept"
Chunk = "org.apache.ctakes.typesystem.type.syntax.Chunk"
NP = "org.apache.ctakes.typesystem.type.syntax.NP"
ADJP = "org.apache.ctakes.typesystem.type.syntax.ADJP"
ADVP = "org.apache.ctakes.typesystem.type.syntax.ADVP"
CONJP = "org.apache.ctakes.typesystem.type.syntax.CONJP"
INTJ = "org.apache.ctakes.typesystem.type.syntax.INTJ"
LST = "org.apache.ctakes.typesystem.type.syntax.LST"
PP = "org.apache.ctakes.typesystem.type.syntax.PP"
PRT = "org.apache.ctakes.typesystem.type.syntax.PRT"
SBAR = "org.apache.ctakes.typesystem.type.syntax.SBAR"
UCP = "org.apache.ctakes.typesystem.type.syntax.UCP"
VP = "org.apache.ctakes.typesystem.type.syntax.VP"
O = "org.apache.ctakes.typesystem.type.syntax.O"
RomanNumeralAnnotation = (
    "org.apache.ctakes.typesystem.type.textsem.RomanNumeralAnnotation"
)
FractionAnnotation = "org.apache.ctakes.typesystem.type.textsem.FractionAnnotation"
DateAnnotation = "org.apache.ctakes.typesystem.type.textsem.DateAnnotation"
TimeAnnotation = "org.apache.ctakes.typesystem.type.textsem.TimeAnnotation"
RangeAnnotation = "org.apache.ctakes.typesystem.type.textsem.RangeAnnotation"
MeasurementAnnotation = (
    "org.apache.ctakes.typesystem.type.textsem.MeasurementAnnotation"
)
PersonTitleAnnotation = (
    "org.apache.ctakes.typesystem.type.textsem.PersonTitleAnnotation"
)
ContextAnnotation = "org.apache.ctakes.typesystem.type.textsem.ContextAnnotation"
LookupWindowAnnotation = (
    "org.apache.ctakes.typesystem.type.textspan.LookupWindowAnnotation"
)
MedicationRoute = "org.apache.ctakes.typesystem.type.refsem.MedicationRoute"
MedicationForm = "org.apache.ctakes.typesystem.type.refsem.MedicationForm"
MedicationStrength = "org.apache.ctakes.typesystem.type.refsem.MedicationStrength"
MedicationDuration = "org.apache.ctakes.typesystem.type.refsem.MedicationDuration"
MedicationDosage = "org.apache.ctakes.typesystem.type.refsem.MedicationDosage"
MedicationFrequency = "org.apache.ctakes.typesystem.type.refsem.MedicationFrequency"
MedicationStatusChange = (
    "org.apache.ctakes.typesystem.type.refsem.MedicationStatusChange"
)
ProcedureDevice = "org.apache.ctakes.typesystem.type.refsem.ProcedureDevice"
ProcedureMethod = "org.apache.ctakes.typesystem.type.refsem.ProcedureMethod"
LabDeltaFlag = "org.apache.ctakes.typesystem.type.refsem.LabDeltaFlag"
LabValue = "org.apache.ctakes.typesystem.type.refsem.LabValue"
LabReferenceRange = "org.apache.ctakes.typesystem.type.refsem.LabReferenceRange"
BodyLaterality = "org.apache.ctakes.typesystem.type.refsem.BodyLaterality"
BodySide = "org.apache.ctakes.typesystem.type.refsem.BodySide"
Course = "org.apache.ctakes.typesystem.type.refsem.Course"
Severity = "org.apache.ctakes.typesystem.type.refsem.Severity"
AnatomicalSite = "org.apache.ctakes.typesystem.type.refsem.AnatomicalSite"
Medication = "org.apache.ctakes.typesystem.type.refsem.Medication"
Procedure = "org.apache.ctakes.typesystem.type.refsem.Procedure"
SignSymptom = "org.apache.ctakes.typesystem.type.refsem.SignSymptom"
DiseaseDisorder = "org.apache.ctakes.typesystem.type.refsem.DiseaseDisorder"
Lab = "org.apache.ctakes.typesystem.type.refsem.Lab"
Element = "org.apache.ctakes.typesystem.type.refsem.Element"
Time = "org.apache.ctakes.typesystem.type.refsem.Time"
Date = "org.apache.ctakes.typesystem.type.refsem.Date"
Event = "org.apache.ctakes.typesystem.type.refsem.Event"
Entity = "org.apache.ctakes.typesystem.type.refsem.Entity"
Attribute = "org.apache.ctakes.typesystem.type.refsem.Attribute"
EventProperties = "org.apache.ctakes.typesystem.type.refsem.EventProperties"
Relation = "org.apache.ctakes.typesystem.type.relation.Relation"
RelationArgument = "org.apache.ctakes.typesystem.type.relation.RelationArgument"
BinaryTextRelation = "org.apache.ctakes.typesystem.type.relation.BinaryTextRelation"
CollectionTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.CollectionTextRelation"
)
UMLSRelation = "org.apache.ctakes.typesystem.type.relation.UMLSRelation"
CoreferenceRelation = "org.apache.ctakes.typesystem.type.relation.CoreferenceRelation"
ElementRelation = "org.apache.ctakes.typesystem.type.relation.ElementRelation"
AttributeRelation = "org.apache.ctakes.typesystem.type.relation.AttributeRelation"
TemporalRelation = "org.apache.ctakes.typesystem.type.relation.TemporalRelation"
Affects = "org.apache.ctakes.typesystem.type.relation.Affects"
ResultOf = "org.apache.ctakes.typesystem.type.relation.ResultOf"
ManifestationOf = "org.apache.ctakes.typesystem.type.relation.ManifestationOf"
LocationOf = "org.apache.ctakes.typesystem.type.relation.LocationOf"
DegreeOf = "org.apache.ctakes.typesystem.type.relation.DegreeOf"
AffectsTextRelation = "org.apache.ctakes.typesystem.type.relation.AffectsTextRelation"
CausesBringsAbout = "org.apache.ctakes.typesystem.type.relation.CausesBringsAbout"
CausesBringsAboutTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.CausesBringsAboutTextRelation"
)
ComplicatesDisrupts = "org.apache.ctakes.typesystem.type.relation.ComplicatesDisrupts"
ComplicatesDisruptsTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.ComplicatesDisruptsTextRelation"
)
Contraindicates = "org.apache.ctakes.typesystem.type.relation.Contraindicates"
ContraindicatesTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.ContraindicatesTextRelation"
)
Diagnoses = "org.apache.ctakes.typesystem.type.relation.Diagnoses"
DiagnosesTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.DiagnosesTextRelation"
)
Indicates = "org.apache.ctakes.typesystem.type.relation.Indicates"
IndicatesTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.IndicatesTextRelation"
)
IsIndicatedFor = "org.apache.ctakes.typesystem.type.relation.IsIndicatedFor"
IsIndicatedForTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.IsIndicatedForTextRelation"
)
ManagesTreats = "org.apache.ctakes.typesystem.type.relation.ManagesTreats"
Prevents = "org.apache.ctakes.typesystem.type.relation.Prevents"
PreventsTextRelation = "org.apache.ctakes.typesystem.type.relation.PreventsTextRelation"
DegreeOfTextRelation = "org.apache.ctakes.typesystem.type.relation.DegreeOfTextRelation"
LocationOfTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.LocationOfTextRelation"
)
ManagesTreatsTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.ManagesTreatsTextRelation"
)
ManifestationOfTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.ManifestationOfTextRelation"
)
ResultOfTextRelation = "org.apache.ctakes.typesystem.type.relation.ResultOfTextRelation"
AspectualTextRelation = (
    "org.apache.ctakes.typesystem.type.relation.AspectualTextRelation"
)
TemporalTextRelation = "org.apache.ctakes.typesystem.type.relation.TemporalTextRelation"
Demographics = "org.apache.ctakes.typesystem.type.structured.Demographics"
SourceData = "org.apache.ctakes.typesystem.type.structured.SourceData"
Metadata = "org.apache.ctakes.typesystem.type.structured.Metadata"
TreebankNode = "org.apache.ctakes.typesystem.type.syntax.TreebankNode"
TerminalTreebankNode = "org.apache.ctakes.typesystem.type.syntax.TerminalTreebankNode"
TopTreebankNode = "org.apache.ctakes.typesystem.type.syntax.TopTreebankNode"
ConllDependencyNode = "org.apache.ctakes.typesystem.type.syntax.ConllDependencyNode"
StanfordDependency = "org.apache.ctakes.typesystem.type.syntax.StanfordDependency"
IdentifiedAnnotation = "org.apache.ctakes.typesystem.type.textsem.IdentifiedAnnotation"
AssertionCuePhraseAnnotation = (
    "org.apache.ctakes.typesystem.type.temporary.assertion.AssertionCuePhraseAnnotation"
)
EntityMention = "org.apache.ctakes.typesystem.type.textsem.EntityMention"
EventMention = "org.apache.ctakes.typesystem.type.textsem.EventMention"
MedicationEventMention = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationEventMention"
)
TimeMention = "org.apache.ctakes.typesystem.type.textsem.TimeMention"
Modifier = "org.apache.ctakes.typesystem.type.textsem.Modifier"
Predicate = "org.apache.ctakes.typesystem.type.textsem.Predicate"
SemanticArgument = "org.apache.ctakes.typesystem.type.textsem.SemanticArgument"
SemanticRoleRelation = "org.apache.ctakes.typesystem.type.textsem.SemanticRoleRelation"
Paragraph = "org.apache.ctakes.typesystem.type.textspan.Paragraph"
List = "org.apache.ctakes.typesystem.type.textspan.List"
ListEntry = "org.apache.ctakes.typesystem.type.textspan.ListEntry"
Pair = "org.apache.ctakes.typesystem.type.util.Pair"
Pairs = "org.apache.ctakes.typesystem.type.util.Pairs"
ProbabilityDistribution = (
    "org.apache.ctakes.typesystem.type.util.ProbabilityDistribution"
)
DocumentClassification = (
    "org.apache.ctakes.typesystem.type.structured.DocumentClassification"
)
MedicationRouteModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationRouteModifier"
)
MedicationFormModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationFormModifier"
)
MedicationStrengthModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationStrengthModifier"
)
MedicationDurationModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationDurationModifier"
)
MedicationDosageModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationDosageModifier"
)
MedicationFrequencyModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationFrequencyModifier"
)
MedicationStatusChangeModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationStatusChangeModifier"
)
ProcedureDeviceModifier = (
    "org.apache.ctakes.typesystem.type.textsem.ProcedureDeviceModifier"
)
ProcedureMethodModifier = (
    "org.apache.ctakes.typesystem.type.textsem.ProcedureMethodModifier"
)
LabDeltaFlagModifier = "org.apache.ctakes.typesystem.type.textsem.LabDeltaFlagModifier"
LabValueModifier = "org.apache.ctakes.typesystem.type.textsem.LabValueModifier"
LabReferenceRangeModifier = (
    "org.apache.ctakes.typesystem.type.textsem.LabReferenceRangeModifier"
)
BodyLateralityModifier = (
    "org.apache.ctakes.typesystem.type.textsem.BodyLateralityModifier"
)
BodySideModifier = "org.apache.ctakes.typesystem.type.textsem.BodySideModifier"
CourseModifier = "org.apache.ctakes.typesystem.type.textsem.CourseModifier"
SeverityModifier = "org.apache.ctakes.typesystem.type.textsem.SeverityModifier"
PolarityModifier = "org.apache.ctakes.typesystem.type.textsem.PolarityModifier"
ConditionalModifier = "org.apache.ctakes.typesystem.type.textsem.ConditionalModifier"
UncertaintyModifier = "org.apache.ctakes.typesystem.type.textsem.UncertaintyModifier"
GenericModifier = "org.apache.ctakes.typesystem.type.textsem.GenericModifier"
SubjectModifier = "org.apache.ctakes.typesystem.type.textsem.SubjectModifier"
HistoryOfModifier = "org.apache.ctakes.typesystem.type.textsem.HistoryOfModifier"
LabInterpretationModifier = (
    "org.apache.ctakes.typesystem.type.textsem.LabInterpretationModifier"
)
MedicationAllergyModifier = (
    "org.apache.ctakes.typesystem.type.textsem.MedicationAllergyModifier"
)
LabEstimatedModifier = "org.apache.ctakes.typesystem.type.textsem.LabEstimatedModifier"
AnatomicalSiteMention = (
    "org.apache.ctakes.typesystem.type.textsem.AnatomicalSiteMention"
)
MedicationMention = "org.apache.ctakes.typesystem.type.textsem.MedicationMention"
ProcedureMention = "org.apache.ctakes.typesystem.type.textsem.ProcedureMention"
SignSymptomMention = "org.apache.ctakes.typesystem.type.textsem.SignSymptomMention"
DiseaseDisorderMention = (
    "org.apache.ctakes.typesystem.type.textsem.DiseaseDisorderMention"
)
LabMention = "org.apache.ctakes.typesystem.type.textsem.LabMention"
Markable = "org.apache.ctakes.typesystem.type.textsem.Markable"
CollectionTextRelationIdentifiedAnnotationRelation = "org.apache.ctakes.typesystem.type.relation.CollectionTextRelationIdentifiedAnnotationRelation"
