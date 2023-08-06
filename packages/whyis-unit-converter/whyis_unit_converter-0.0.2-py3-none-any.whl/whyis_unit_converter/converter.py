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

from .unit_converter import convert_attr_to_units, is_a_convertible_unit_attr

class UnitConverter(autonomic.UpdateChangeService):
    activity_class = whyis.UnitConverter

    def getInputClass(self):
        return sio.Entity

    def getOutputClass(self):
        return URIRef("StandardizedConversionEntity")

    def get_query(self):
        query = '''SELECT ?s WHERE {
    ?s <http://semanticscience.org/resource/hasAttribute> ?a . 
    ?a <http://semanticscience.org/resource/hasUnit> []; 
       <http://semanticscience.org/resource/hasValue> [] .
}'''
        return query

    def process(self, i, o):
        for attr in i.objects(sio.hasAttribute):
            if is_a_convertible_unit_attr(attr):
                converted = convert_attr_to_units(attr)
                activity = BNode()
                for new_meas in converted:
                    # Add new measurement to graph, note provenance of new data
                    o.add(sio.hasAttribute, new_meas)
                    o.graph.add((new_meas.identifier, prov.wasGeneratedBy, activity))
                    o.graph.add((activity, prov.used, attr.identifier))
                    o.graph.add((activity, prov.generated, new_meas.identifier))
                    o.graph.add((activity, prov.atTime, Literal(util.date_time(t=time()))))
                    o.graph.add((activity, prov.wasAssociatedWith, URIRef("http://nanomine.org/ns/WhyisUnitConverterV001")))

                    # Add all triples for the measurement
                    for p_, o_ in new_meas.predicate_objects():
                        if isinstance(o_, Resource):
                            o.graph.add((new_meas.identifier, p_.identifier, o_.identifier))
                        else:
                            o.graph.add((new_meas.identifier, p_.identifier, o_))
