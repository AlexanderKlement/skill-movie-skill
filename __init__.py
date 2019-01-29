#!/usr/bin/env python
# -*- coding: utf-8 -*

from mycroft import MycroftSkill, intent_file_handler
from SPARQLWrapper import SPARQLWrapper, JSON, POSTDIRECTLY
from string import Template
from rdflib import Graph
from .graph import Graph as g
import sys
WRAPPER = "http://graphdb.sti2.at:8080/repositories/broker-graph"
GRAPH_LINK = "https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest"
#newer link:
#https://broker.semantify.it/graph/O68LFbndcM/WHn3NHFiml/latest



class SkillMovie(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.director = "I do not know who directed that"
        self.actor = "I do not know who acted in there"

    @intent_file_handler('director.intent')
    def handle_movie_skill(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?director_name
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name "$movie_name".
                ?movie schema:director ?director.
                ?director schema:name ?director_name.
            }
        """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            self.director = result["director_name"]["value"]
        self.speak_dialog('director', data={'movie': movie, 'director': self.director})

    @intent_file_handler('actor.intent')
    def handle_movie_skill(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
                PREFIX schema: <http://schema.org/>
                SELECT ?actor_name
                FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
                WHERE {
                    ?movie a schema:Movie.
                    ?movie schema:name "$movie_name".
                    ?movie schema:actor ?actor.
                    ?actor schema:name ?actor_name.
                }
            """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            self.actor = result["actor_name"]["value"]
        self.speak_dialog('actor', data={'movie': movie, 'actor': self.actor})


def create_skill():
    return SkillMovie()
