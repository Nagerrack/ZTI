from SPARQLWrapper import SPARQLWrapper, JSON


def get_url_by_name(word):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """PREFIX dbo:  <http://dbpedia.org/ontology/>
      PREFIX dbpedia: <http://dbpedia.org/resource/>
      SELECT DISTINCT ?subject ?type               
      WHERE{ 
       ?subject rdf:type ?type.
        ?subject rdfs:label ?label.
       ?label bif:contains "'""" + word + """'"@en
      }
      LIMIT 500"""

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    print(results)

    try:
        url = [result['subject']['value'] for result in
               results["results"]["bindings"]]
        word = word.replace('.', '')
        word = word.replace(',', '')
        word = word.replace(' ', '_')
        url = [u for u in url if 'dbpedia' and 'resource' and word in u
               and len(u) >= len('http://dbpedia.org/resource/' + word) and
               u.replace('http://dbpedia.org/resource/', '')[0] == word[0]]
        url.sort(key=lambda x: len(x))
        final_url = url[0]
    except:
        final_url = "No data found"

    return final_url


def get_url_by_name_with_specified_type(word, entity_type):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """PREFIX dbo:  <http://dbpedia.org/ontology/>
      PREFIX dbpedia: <http://dbpedia.org/resource/>
      SELECT DISTINCT ?subject ?type               
      WHERE{ 
       ?subject rdf:type ?type.
        ?subject rdfs:label ?label.
       ?label bif:contains "'""" + word + """'"@en
        FILTER (?type = dbo:""" + entity_type + """)
      }
      LIMIT 100"""

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    print(results)

    try:
        url = [result['subject']['value'] for result in
               results["results"]["bindings"]]
        url = [u for u in url if 'dbpedia' in u]
        url.sort(key=lambda x: len(x))
        final_url = url[0]
    except:
        final_url = "No data found"

    return final_url


# def get_url_by_name(word):
#     sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#     query = """
#             PREFIX dbo:  <http://dbpedia.org/ontology/>
#             PREFIX dbpedia: <http://dbpedia.org/resource/>
#             SELECT DISTINCT ?s
#             WHERE{
#                ?s ?k ?v.
#                FILTER regex(?s, '""" + word + """')
#             }"""
#
#     # OLD FILTER (?s = dbpedia:""" + word + """)
#     # FILTER regex(?s, """+ word +""")
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#
#     try:
#         url = results["results"]["bindings"][0]["s"]["value"]
#     except:
#         url = "No data found"
#
#     return url


def get_types_from_db(word):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
                PREFIX dbo:  <http://dbpedia.org/ontology/>
                PREFIX dbpedia: <http://dbpedia.org/resource/>
                SELECT DISTINCT ?subject ?type
                WHERE{ 
                   ?subject rdf:type ?type .
                   FILTER (?subject
                    = dbpedia:""" + word + """)
                   FILTER regex(?type, "http://dbpedia.org/ontology/")
                }"""

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    try:
        url = [result['type']['value'].replace('http://dbpedia.org/ontology/', '') for result in
               results["results"]["bindings"]]
    except:
        url = "{} : No data found".format(word)

    return url


def get_name_by_type(type, number):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
                    PREFIX dbo:  <http://dbpedia.org/ontology/>
                    PREFIX dbpedia: <http://dbpedia.org/resource/>
                    SELECT ?subject
                    WHERE{ 
                       ?subject rdf:type ?type.
                       FILTER (?type = dbo:""" + type + """)
                    }
                    limit %d""" % number

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    try:
        name = [result['subject']['value'].replace('http://dbpedia.org/resource/', '') for result in
                results["results"]["bindings"]]
    except:
        name = "{} : No data found".format(type)

    return name


def get_url_by_type(type, number):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
                    PREFIX dbo:  <http://dbpedia.org/ontology/>
                    PREFIX dbpedia: <http://dbpedia.org/resource/>
                    SELECT ?subject
                    WHERE{ 
                       ?subject rdf:type ?type.
                       FILTER (?type = dbo:""" + type + """)
                    }
                    limit %d""" % number

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    try:
        url = [result['subject']['value'] for result in
               results["results"]["bindings"]]
    except:
        url = "{} : No data found".format(type)

    return url


def get_types_by_url(url):
    resource = url.replace('http://dbpedia.org/resource/', '')
    resource = resource.replace('.', '')
    resource = resource.replace("'", '')
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
                    PREFIX dbo:  <http://dbpedia.org/ontology/>
                    PREFIX dbpedia: <http://dbpedia.org/resource/>
                    SELECT DISTINCT ?subject ?type
                    WHERE{ 
                        ?subject rdf:type ?type .
                   FILTER (?subject
                    = dbpedia:""" + resource + """)
                   FILTER regex(?type, "http://dbpedia.org/ontology/")
                    }"""

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    try:
        types = [result['type']['value'].replace('http://dbpedia.org/ontology/', '') for result in
                 results["results"]["bindings"]]
    except:
        types = "{} : No data found".format(resource)

    return types
