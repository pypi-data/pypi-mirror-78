""" Provides a testing framework for the Unit Conversion agent."""

from rdflib import *

from whyis_unit_converter import unit_converter_agent as converter

from whyis import nanopub

from whyis.namespace import sio
from whyis.test.agent_unit_test_case import AgentUnitTestCase

om = Namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")

class UnitConverterAgentTestCase(AgentUnitTestCase):

    def test_conversion(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:0",
      "@type": [ "http://nanomine.org/ns/Width" ],
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://nanomine.org/ns/unit/nm",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "Nanometer"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 50} ]
    }
  ]
        }''', format="json-ld")
        np.assertion.parse(data='''{
  "@id": "http://nanomine.org/ns/Width",
  "http://nanomine.org/ns/hasPreferredUnit": "http://www.ontology-of-units-of-measure.org/resource/om-2/micrometre"
        }''', format="json-ld")

        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 1)
        # print("Printing agent results:\n\n", results[0].serialize(format="trig"), "\n")

        contains_micrometre = False
        correct_micrometre_value = False
        if len(results) > 0:
            for attr in results[0].resource(URIRef("http://example.com/converter_test"))[sio.hasAttribute]:
                if attr[sio.hasUnit : om.micrometre]:
                    contains_micrometre = True
                    if attr[sio.hasValue : Literal(0.05)]:
                        correct_micrometre_value = True

        self.assertTrue(contains_micrometre)
        self.assertTrue(correct_micrometre_value)

    def test_no_conversion(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:253f65a70d014043be04c2b8583c174d",
      "@type": [ "http://nanomine.org/ns/CurrentDensity" ],
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://www.ontology-of-units-of-measure.org/resource/om-2/amperePerSquareMetre",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "A/m^2"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 4.713376e-08} ]
    }
  ]
}''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)

    def test_conversion_to_incompatible_units(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:1",
      "@type": "http://nanomine.org/ns/FiberTensileStrength",
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://www.ontology-of-units-of-measure.org/resource/om-2/voltPerMetre",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "Volts per Meter"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 0.3} ]
    }
  ]
}''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)

    def test_no_value(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:14626f9a927b4e7a980f802676b42402",
      "@type": [ "http://nanomine.org/ns/AC_DielectricDispersion" ]
    }
  ]
}''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)

    def test_bad_unit(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:3",
      "@type": "http://nanomine.org/ns/GlassTransitionTemperature",
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://example.com/badUnit",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "Kelvin"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 250} ]
    }
  ]
}''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)

    def test_bad_value(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:4",
      "@type": "http://nanomine.org/ns/GlassTransitionTemperature",
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://www.ontology-of-units-of-measure.org/resource/om-2/kelvin",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "Kelvin"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": "a"} ]
    }
  ]
}''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)

    def test_bad_unit_type(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:2",
      "@type": "http://example.com/badUnitType",
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://www.ontology-of-units-of-measure.org/resource/om-2/kelvin",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "Kelvin"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 250} ]
    }
  ]
}
''', format="json-ld")

        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)

    def test_lack_of_preferred_unit(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:0",
      "@type": [ "http://nanomine.org/ns/Width" ],
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://nanomine.org/ns/unit/nm",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "Nanometer"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 50} ]
    }
  ]
        }''', format="json-ld")

        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)

    def test_already_converted(self):
        np = nanopub.Nanopublication()
        np.assertion.parse(data='''{
  "@id": "http://example.com/converter_test",
  "@type": [ "http://nanomine.org/ns/PolymerNanocomposite" ],
  "http://semanticscience.org/resource/hasAttribute": [
    {
      "@id": "bnode:0",
      "@type": [ "http://nanomine.org/ns/Width" ],
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://nanomine.org/ns/unit/nm",
          "http://www.w3.org/2000/01/rdf-schema#label": [ {"@value": "Nanometer"} ]
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 50} ]
    },
    {
      "@id": "bnode:1",
      "@type": [ "http://nanomine.org/ns/Width" ],
      "http://semanticscience.org/resource/hasUnit": [
        {
          "@id": "http://www.ontology-of-units-of-measure.org/resource/om-2/micrometre"
        }
      ],
      "http://semanticscience.org/resource/hasValue": [ {"@value": 0.05} ],
      "http://www.w3.org/ns/prov#wasDerivedFrom": [ {"@id": "bnode:0"} ]
    }
  ]
        }''', format="json-ld")
        np.assertion.parse(data='''{
  "@id": "http://nanomine.org/ns/Width",
  "http://nanomine.org/ns/hasPreferredUnit": "http://www.ontology-of-units-of-measure.org/resource/om-2/micrometre"
        }''', format="json-ld")
        # print(np.serialize(format="trig"))
        agent = converter.UnitConverter()
        results = self.run_agent(agent, nanopublication=np)

        self.assertEquals(len(results), 0)
