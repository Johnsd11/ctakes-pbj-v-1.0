import create_type as ct
import jcas_processor
from ctakes_types import *


class ExampleWordFinder(jcas_processor.JCasProcessor):

    def process_jcas(self, cas, typesystem):

        #  While we could use ct.create_type to create and add types, for each type lookup the cas array is searched.
        #  So it is faster to get the types first and then create instances with ct.add_type
        anatomy_type = typesystem.get_type(AnatomicalSiteMention)
        symptom_type = typesystem.get_type(SignSymptomMention)
        procedure_type = typesystem.get_type(ProcedureMention)

        sites = ['breast']
        findings = ['hernia', 'pain', 'migraines', 'allergies']
        procedures = ['thyroidectomy', 'exam']

        for segment in cas.select(Segment):
            text = segment.get_covered_text()
            for word in sites:
                begin = text.find(word)
                if begin > -1:
                    print("found something")
                    end = begin + len(word)
                    ct.add_type(cas, anatomy_type, begin, end)
            for word in findings:
                begin = text.find(word)
                if begin > -1:
                    print("found something2")
                    end = begin + len(word)
                    ct.add_type(cas, symptom_type, begin, end)
            for word in procedures:
                begin = text.find(word)
                if begin > -1:
                    print("found something3")
                    end = begin + len(word)
                    ct.add_type(cas, procedure_type, begin, end)
