import cas_annotator
from ctakes_types import *
import asyncio
# from cnlpt.api.dtr_rest import *
from cnlpt.api.dtr_rest import startup_event as dtr_init
from cnlpt.api.dtr_rest import process as dtr_process
from cnlpt.api.cnlp_rest import EntityDocument
import cnlpt.api.dtr_rest as dtr_rest
import time

from pprint import pprint

sem = asyncio.Semaphore(1)


class ExampleDtr(cas_annotator.CasAnnotator):

    def initialize(self):
        # startup_event()
        print("starting init " + str(time.time()))
        asyncio.run(self.init_caller())

        print("done with init " + str(time.time()))

    def process(self, cas):
        print("processing")
        # process_url = 'http://localhost:8000/negation/process'

        eventMentions = cas.select(EventMention)
        sites = cas.select(AnatomicalSiteMention)
        entities = eventMentions + sites

        t = []
        for e in entities:
            t.append([e.begin, e.end])

        # eDoc = EntityDocument(doc_text=cas.sofa_string, entities=t)
        # dtr_output = self.dtr_caller(cas.sofa_string, t)
        # print(dtr_output)
        print("calling dtr caller" + str(time.time()))
        asyncio.run(self.dtr_caller(cas.sofa_string, t))
        print("done calling dtr " + str(time.time()))

    async def init_caller(self):
        await dtr_rest.startup_event()


    async def dtr_caller(self, text, t):
        eDoc = EntityDocument(doc_text=text, entities=t)

        #async with sem:
        dtr_output = await dtr_rest.process(eDoc)
        #for future in asyncio.as_completed(dtr_rest.process(eDoc)):
           # dtr_output = await future
        print("output:" + repr(dtr_output))
           # print(dtr_output.statuses)
        #return dtr_output