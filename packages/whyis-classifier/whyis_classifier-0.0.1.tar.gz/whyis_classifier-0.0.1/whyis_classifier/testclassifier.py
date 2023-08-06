from .whyisclassifier import WhyisClassifier
from rdflib import URIRef

from rdflib.namespace import RDF

class TestClassifier(WhyisClassifier):
    identifier = URIRef("http://test.org/testclassifier")
    def label(self, sample):
        for t in sample[RDF.type]:
            if str(t.identifier) == "http://test.org/PNC":
                return "http://test.org/ItsAPNC", 1
        return URIRef("http://test.org/NotAPNC"), None
