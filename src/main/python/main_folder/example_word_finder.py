import jcas_processor
from ctakes_types import *


class ExampleWordFinder(jcas_processor.JCasProcessor):

    def __init__(self, type_system):
        self.type_system = type_system

    def process_jcas(self, cas):

        Anatomy = self.type_system.get_type(AnatomicalSiteMention)
        Symptom = self.type_system.get_type(SignSymptomMention)
        Procedure = self.type_system.get_type(ProcedureMention)

        sites = ['breast']
        findings = ['hernia', 'pain',  'migraines', 'allergies']
        procedures = ['thyroidectomy', 'exam']

        for segment in cas.select(Segment):
            text = segment.get_covered_text()
            for word in sites:
                begin = text.find(word)
                if begin > -1:
                    print("found something")
                    end = begin + len(word)
                    site = Anatomy(begin=begin, end=end)
                    cas.add_annotation(site)
            for word in findings:
                begin = text.find(word)
                if begin > -1:
                    print("found something2")
                    end = begin + len(word)
                    finding = Symptom(begin=begin, end=end)
                    cas.add_annotation(finding)
            for word in procedures:
                begin = text.find(word)
                if begin > -1:
                    print("found something3")
                    end = begin + len(word)
                    procedure = Procedure(begin=begin, end=end)
                    cas.add_annotation(procedure)
