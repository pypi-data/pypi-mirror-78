""" Unit Conversion Agent for Whyis
    Uses <http://tetherless-world.github.io/whyis/inference>
    as a template.
"""

from __future__ import division
from past.utils import old_div
import nltk, re, pprint
from rdflib import *
from rdflib.resource import Resource
from time import time

from whyis import autonomic
from whyis import nanopub
from whyis.namespace import sioc_types, sioc, sio, dc, prov, whyis

from .attr_converter import convert_attr_to_units

class UnitConverter(autonomic.GlobalChangeService):
    activity_class = URIRef("http://nanomine.org/ns/WhyisUnitConverterV002")

    def getInputClass(self):
        return sio.Entity

    def getOutputClass(self):
        return URIRef("StandardizedConversionEntity")

    def get_query(self):
        query = '''SELECT ?s WHERE {
    ?s <http://semanticscience.org/resource/hasAttribute> ?attr.
    ?attr <http://semanticscience.org/resource/hasUnit> [];
          <http://semanticscience.org/resource/hasValue> [];
          a [ <http://nanomine.org/ns/hasPreferredUnit> ?prefUnit ].
}'''
        return query

    def process(self, i, o):
        for attr in i.objects(sio.hasAttribute):
            converted = convert_attr_to_units(attr)
            if converted is not None:
                activity = BNode()
                for new_meas in converted:
                    # Add new measurement to graph
                    o.add(sio.hasAttribute, new_meas)
                    # note provenance of new data--SUPERSEDED by superclass's explain() function
                    # o.graph.add((new_meas.identifier, prov.wasGeneratedBy, activity))
                    # o.graph.add((activity, prov.used, attr.identifier))
                    # o.graph.add((activity, prov.generated, new_meas.identifier))
                    # o.graph.add((activity, prov.atTime, Literal(util.date_time(t=time()))))
                    # o.graph.add((activity, prov.wasAssociatedWith, URIRef("http://nanomine.org/ns/WhyisUnitConverterV002")))

                    # Add all triples for the measurement
                    for p_, o_ in new_meas.predicate_objects():
                        if isinstance(o_, Resource):
                            o.graph.add((new_meas.identifier, p_.identifier, o_.identifier))
                        else:
                            o.graph.add((new_meas.identifier, p_.identifier, o_))
