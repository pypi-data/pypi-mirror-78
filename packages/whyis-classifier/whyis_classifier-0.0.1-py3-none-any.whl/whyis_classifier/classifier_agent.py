""" Classification Agent for Whyis
    Uses <http://tetherless-world.github.io/whyis/inference>
    as a template.
"""

from __future__ import division
from past.utils import old_div
import nltk, re, pprint
from rdflib import *
from rdflib.resource import Resource
import logging


from whyis import autonomic
from whyis import nanopub
from whyis.namespace import sioc_types, sioc, sio, dc, prov, whyis

from rdflib.namespace import RDF
from rdflib.term import Node
from .user_classifiers import user_classifiers

class Classifier(autonomic.GlobalChangeService):
    activity_class = URIRef("http://nanomine.org/ns/WhyisClassifierV001")
    classifiers = dict(user_classifiers)

    def getInputClass(self):
        return sio.Entity

    def getOutputClass(self):
        return sio.Entity

    def get_query(self):
        query = '''SELECT ?s WHERE {
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://nanomine.org/ns/PolymerNanocomposite> .
}'''
        return query

    # kept for minimal functionality if process_graph must be changed
    # cannot label the assertion with a confidence, or include provenance
    # from individual classifiers. use updated process_graph if at all possible
    def process(self, i, o):
        for classifier_name in self.classifiers:
            classifier = self.classifiers[classifier_name]
            label, confidence = classifier.label(i)
            if label == "":
                continue
            if not isinstance(label, Node):
                label = URIRef(label)
            o.add(RDF.type, label)

    # mostly copied from superclass whyis.autonomic.Service on August 20, 2020
    def process_graph(self, inputGraph):
        # repeat processing for every user classifier
        for classifier_name in self.classifiers:
            classifier = self.classifiers[classifier_name]
            instances = self.getInstances(inputGraph)
            results = []
            for i in instances:
                print("Processing", i.identifier, self)
                output_nanopub = self.app.nanopub_manager.new()
                o = output_nanopub.assertion.resource(i.identifier)  # OutputClass(i.identifier)
                error = False
                try:
                    ### CLASSIFIER CODE
                    # replaced call to process_nanopub in order to include the
                    # provenance of the individual classifier
                    label, confidence = classifier.label(i)
                    if label == "":
                        continue
                    if not isinstance(label, Node):
                        label = URIRef(label)
                    o.add(RDF.type, label)
                    if confidence is not None:
                        output_nanopub.provenance.add(
                            (output_nanopub.assertion.identifier, sio.SIO_000638, Literal(confidence)))
                    ### END CLASSIFIER CODE
                except Exception as e:
                    output_nanopub.add(
                        (output_nanopub.assertion.identifier, self.app.NS.sioc.content, Literal(str(e))))
                    logging.exception("Error processing resource %s in nanopub %s" % (i.identifier, inputGraph.identifier))
                    error = True
                for new_np in self.app.nanopub_manager.prepare(ConjunctiveGraph(store=output_nanopub.store)):
                    if len(new_np.assertion) == 0 and not error:
                        continue
                    ### CLASSIFIER CODE
                    # includes extra parameter to include classifier in provenance
                    self.explain(new_np, i, o, classifier.identifier)
                    ### END CLASSIFIER CODE
                    new_np.add((new_np.identifier, sio.isAbout, i.identifier))
                    # print new_np.serialize(format="trig")
                    if not self.dry_run:
                        self.app.nanopub_manager.publish(new_np)
                    else:
                        print("Not publishing",new_np.identifier,", dry run.")
                    results.append(new_np)
        return results

    # mostly copied from superclass whyis.autonomic.Service on August 20, 2020
    # added parameter of classifier's identifier
    def explain(self, nanopub, i, o, classifier):
        activity = nanopub.provenance.resource(BNode())
        activity.add(RDF.type, self.activity_class)
        # only change to the function is this line (and additional parameter)
        activity.add(prov.wasAssociatedWith, classifier)
        nanopub.pubinfo.add((o.identifier, RDF.type, self.getOutputClass()))
        nanopub.provenance.add((nanopub.assertion.identifier, prov.wasGeneratedBy, activity.identifier))
