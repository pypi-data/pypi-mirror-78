from rdflib import URIRef

class WhyisClassifier():
    """ Base class for the Whyis Classifier."""
    identifier = URIRef("http://nanomine.org/ns/generic_whyis_classifier")

    def label(self, sample):
        """ Return a label and a confidence score, to be applied to the given sample.
            Can classify the sample based on any attributes of the sample itself.

            label: a label to add to the knowledge graph.
                Can be a URI string, or an rdflib.URIRef object.
                Cannot be an empty string.
            confidence: a score for the label, a number between 0 and 1 or None.
                Can be None, if no score is computed/provided. If the score is None,
                it will not be added to the knowledge graph

                example: "http://nanomine.org/ns/Elastomer", 0.7
        """
        label = ""
        confidence = None
        return label, confidence
