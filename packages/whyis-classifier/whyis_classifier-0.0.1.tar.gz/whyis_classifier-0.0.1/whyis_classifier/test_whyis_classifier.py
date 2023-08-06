""" Provides a testing framework for the Classifier Agent."""

from rdflib import *
from rdflib.namespace import RDF

from whyis_classifier import classifier_agent as ca
from whyis_classifier import testclassifier
from whyis_classifier import whyisclassifier

from whyis import nanopub
from whyis.test.agent_unit_test_case import AgentUnitTestCase
from whyis.namespace import sio


class ClassifierAgentTestCase(AgentUnitTestCase):
    def test_positive_classifier(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
        "@id": "http://test.org/test_data",
        "@type": [ "http://nanomine.org/ns/PolymerNanocomposite",
                   "http://test.org/PNC" ]
        }''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = ca.Classifier()
        # replace any user-defined classifiers with test classifier
        agent.classifiers = {'test_classifier': testclassifier.TestClassifier()}
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 1)
        # print(results[0].serialize(format='trig'))

        labeled_correctly = False
        confidence = None
        if results[0].resource(URIRef("http://test.org/test_data"))[RDF.type : URIRef("http://test.org/ItsAPNC")]:
            labeled_correctly = True
        for conf in results[0].objects(subject=None, predicate=sio.SIO_000638):
            confidence = conf.value

        self.assertEquals(confidence, 1)
        self.assertTrue(labeled_correctly)

    def test_negative_classifier(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
        "@id": "http://test.org/test_data",
        "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ]
        }''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = ca.Classifier()
        # replace any user-defined classifiers with test classifier
        agent.classifiers = {'test_classifier': testclassifier.TestClassifier()}
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 1)
        # print(results[0].serialize(format='trig'))

        labeled_correctly = False
        confidence = None
        if results[0].resource(URIRef("http://test.org/test_data"))[RDF.type : URIRef("http://test.org/NotAPNC")]:
            labeled_correctly = True
        for conf in results[0].objects(subject=None, predicate=sio.SIO_000638):
            confidence = conf.value
        self.assertIsNone(confidence)

        self.assertTrue(labeled_correctly)
