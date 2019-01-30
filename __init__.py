#!/usr/bin/env python
# -*- coding: utf-8 -*

from mycroft import MycroftSkill, intent_file_handler
from SPARQLWrapper import SPARQLWrapper, JSON, POSTDIRECTLY
from string import Template
from rdflib import Graph
from .graph import Graph as g
import random
WRAPPER = "http://graphdb.sti2.at:8080/repositories/broker-graph"
GRAPH_LINK = "https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest"
#newer link:
#https://broker.semantify.it/graph/O68LFbndcM/WHn3NHFiml/latest



class SkillMovie(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.director = "not known by me"
        self.actor = "a stranger to me"
        self.description = "no description available"
        self.duration = "unknown length"
        self.release = "unknown release date"
        self.productionStudio = "unknown production studio"
        self.production= "unknown country"
        self.genre= "none"
        self.movie= "none"

    def initialize(self):
        self.register_intent_file("director.intent", self.handle_director)
        self.register_intent_file("actor.intent", self.handle_actor)
        self.register_intent_file("description.intent", self.handle_description)
        self.register_intent_file("duration.intent", self.handle_duration)
        self.register_intent_file("release.intent", self.handle_release)
        self.register_intent_file("productionStudio.intent", self.handle_productionStudio)
        self.register_intent_file("production.intent", self.handle_production)
        self.register_intent_file("directorOfMovie.intent", self.handle_directorOfMovie)
        self.register_intent_file("genre.intent", self.handle_genre)

    @intent_file_handler('director.intent')
    def handle_director(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?director_name
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name ?movie_name.
                ?movie schema:director ?director.
                ?director schema:name ?director_name.
                $regex
            }
        """)
        regex = ""
        for i in range(len(movie.split())):
            regex += "FILTER regex(?movie_name, \"" + movie.split()[i] + "\", \" i \").\n"
        print(regex)
        sparql.setQuery(qt.substitute({"regex": regex}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            self.director = result["director_name"]["value"]
        self.speak_dialog('director', data={'movie': movie, 'director': self.director})

    @intent_file_handler('actor.intent')
    def handle_actor(self, message):
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


    @intent_file_handler('description.intent')
    def handle_description(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?description
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name "$movie_name".
                ?movie schema:description ?description.
                }
            """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            self.description = result["description"]["value"]
        self.speak_dialog('description', data={'movie': movie, 'description': self.description})


    @intent_file_handler('duration.intent')
    def handle_duration(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?duration
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name "$movie_name".
                ?movie schema:duration ?duration.
                }
            """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
        for result in results["results"]["bindings"]:
            self.duration = result["duration"]["value"]
            print(self.duration)
        self.speak_dialog('duration', data={'movie': movie, 'duration': self.duration})

    @intent_file_handler('duration.intent')
    def handle_duration(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?duration
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name "$movie_name".
                ?movie schema:duration ?duration.
                }
            """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
        for result in results["results"]["bindings"]:
            self.duration = result["duration"]["value"]
        self.speak_dialog('duration', data={'movie': movie, 'duration': self.duration})

    @intent_file_handler('release.intent')
    def handle_release(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?datePublished
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name "$movie_name".
                ?movie schema:datePublished ?datePublished.
            }
            """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
        for result in results["results"]["bindings"]:
            self.release = result["datePublished"]["value"]
        self.speak_dialog('release', data={'movie': movie, 'release': self.release})

    @intent_file_handler('productionStudio.intent')
    def handle_productionStudio(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?name
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name "$movie_name".
                ?movie schema:productionCompany ?productionCompany.
                ?productionCompany schema:name ?name.
            }
            """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
        for result in results["results"]["bindings"]:
            self.productionStudio = result["name"]["value"]
        self.speak_dialog('productionStudio', data={'movie': movie, 'productionStudio': self.productionStudio})

    @intent_file_handler('production.intent')
    def handle_production(self, message):
        movie = message.data["movie"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
                PREFIX schema: <http://schema.org/>
                SELECT ?name
                FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
                WHERE {
                    ?movie a schema:Movie.
                    ?movie schema:name "$movie_name".
                    ?movie schema:countryOfOrigin ?country.
                    ?country schema:name ?name.
                }
                """)
        sparql.setQuery(qt.substitute({"movie_name": movie}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
        for result in results["results"]["bindings"]:
            self.production = result["country"]["value"]
        self.speak_dialog('production', data={'movie': movie, 'production': self.production})


    @intent_file_handler('directorOfMovie.intent')
    def handle_directorOfMovie(self, message):
        movie = message.data["movie"]
        director = message.data["director"]
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
        print(results)
        for result in results["results"]["bindings"]:
            self.director = result["director_name"]["value"]
        if(director.lower() == self.director.lower()):
            self.speak_dialog('directorOfMovie', data={'movie': movie, 'director': director})
        else:
            self.speak_dialog('notDirectorOfMovie', data={'movie': movie, 'director': director})


    @intent_file_handler('actorOfMovie.intent')
    def handle_actorOfMovie(self, message):
        movie = message.data["movie"]
        actor = message.data["actor"]
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
        print(results)
        for result in results["results"]["bindings"]:
            self.actor = result["actor_name"]["value"]
            if (actor.lower() == self.actor.lower()):
                self.speak_dialog('actorOfMovie', data={'movie': movie, 'actor': actor})
                return
        self.speak_dialog('notActorOfMovie', data={'movie': movie, 'actor': actor})

    @intent_file_handler('genre.intent')
    def handle_genre(self, message):
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT ?genre
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:genre ?genre.
            }
            """)
        sparql.setQuery(qt.substitute())
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        self.genre = []
        for result in results["results"]["bindings"]:
            self.genre.append(result["genre"]["value"])
        set(self.genre)
        self.speak_dialog('genre', data={'genre': self.genre})

    @intent_file_handler('suggestByGenre.intent')
    def handle_suggestByGenre(self, message):
        genre = message.data["genre"]
        sparql = SPARQLWrapper("http://graphdb.sti2.at:8080/repositories/broker-graph")
        qt = Template("""
            PREFIX schema: <http://schema.org/>
            SELECT *
            FROM <https://broker.semantify.it/graph/O89n4PteKl/Wc8XrLETTj/latest>
            WHERE {
                ?movie a schema:Movie.
                ?movie schema:name ?movie_name.
                ?movie schema:genre ?genre.
            }
            """)
        sparql.setQuery(qt.substitute({'genre': genre}))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
        self.movie = []
        for result in results["results"]["bindings"]:
            if (result["genre"]["value"]).lower() == genre.lower():
                self.movie.append(result["movie_name"]["value"])
        self.movie = self.movie[random.randint(0, len(self.movie) - 1)]
        self.speak_dialog('suggestByGenre', data={'movie': self.movie})

def create_skill():
    return SkillMovie()
