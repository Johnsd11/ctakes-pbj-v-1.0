import cas_annotator
from ctakes_types import *
import requests
from pprint import pprint


class ExampleTemporalRest(cas_annotator.CasAnnotator):

    def process(self, cas):

        process_url = 'http://localhost:8000/temporal/process_sentence'
        event_type = cas.typesystem.get_type(Event)
        event_properties_type = cas.typesystem.get_type(EventProperties)

        for sentence in cas.select(Sentence):
            text = sentence.get_covered_text()
            r = requests.post(process_url, json={'sentence': text})
            pprint(r.json())

