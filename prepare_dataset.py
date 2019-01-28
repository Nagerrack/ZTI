import rdflib as rd
from rdflib import Namespace

from configuration_data import types
from sparql_queries import get_types_by_url

nif_header = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
rdf_header = Namespace("http://www.w3.org/2005/11/its/rdf#")


class TrainSample:

    def __init__(self, sentence):
        self.sentence = sentence
        self.associated_entities = []

    def __str__(self):
        return "[{0}]: {1}".format(self.sentence, self.associated_entities)

    def add_entity(self, entity):
        self.associated_entities.append(entity)


def graph_to_train_samples(graph):
    train_samples = []
    for reference in graph.subjects(object=nif_header.Context):
        for sentence_object in graph.objects(subject=reference, predicate=nif_header.isString):
            new_sample = TrainSample(sentence_object)
            train_samples.append(new_sample)

        for entity_subject in graph.subjects(predicate=nif_header.referenceContext, object=reference):
            url, name, begin_index, end_index = None, None, None, None
            for phrase in graph.predicate_objects(subject=entity_subject):
                if 'taIdentRef' in phrase[0]:
                    url = str(phrase[1])
                if 'anchorOf' in phrase[0]:
                    name = str(phrase[1])
                if 'beginIndex' in phrase[0]:
                    begin_index = int(phrase[1])
                if 'endIndex' in phrase[0]:
                    end_index = int(phrase[1])

            train_samples[-1].add_entity([name, url, begin_index, end_index])

    return [s for s in train_samples if len(s.associated_entities) != 0]


def get_type_from_db(url):
    if 'aksw' in url:
        return 'Not_on_wiki'
    # if ',' or '(' or ')' in url:
    #     return 'Not_on_wiki'
    url = url.replace(',', '')
    url = url.replace('(', '')
    url = url.replace(')', '')
    # if re.search('/[0-9]*[A-z]*_*.[0-9]*[A-z]*_*$', url) is not None:
    #     return 'Not_on_wiki'

    db_types = get_types_by_url(url)
    mutual_types = set(types).intersection(db_types)
    if len(mutual_types) > 0:
        entity_type = mutual_types.pop()
    else:
        entity_type = 'Not_found'
    return entity_type


def get_type_from_db_corrected(url):
    db_types = get_types_by_url(url)
    mutual_types = set(types).intersection(db_types)
    if len(mutual_types) > 0:
        entity_type = mutual_types.pop()
    else:
        entity_type = 'Not_found'
    return entity_type


def find_next(string, substrings, begin_pos):
    for index, char in enumerate(string[begin_pos:]):
        if char in substrings:
            return begin_pos + index
    return -1


def create_and_save_dataset(corpus_name):
    g = rd.Graph()
    g.parse(r'oke17task2Training.xml.ttl', format='turtle')
    sentences = graph_to_train_samples(g)
    with open(corpus_name, 'w', encoding='utf-8') as corpus_file:
        for sentence in sentences:
            begin_pos = 0
            end_pos = find_next(sentence.sentence, ['.', ',', '!', '?', ':', ';', '"', '“', '”', ' '], begin_pos)
            while end_pos != -1:
                word = sentence.sentence[begin_pos:end_pos]
                is_entity = 0
                if begin_pos != end_pos:
                    for entity in sentence.associated_entities:
                        if begin_pos >= entity[2] and end_pos <= entity[3]:
                            is_entity = 1
                            entity_type = get_type_from_db(entity[1])
                            corpus_file.write('{0}\t{1}\n'.format(word, entity_type))
                            print(word, entity[1])
                            break
                    if is_entity == 0:
                        corpus_file.write('{0}\t{1}\n'.format(word, 'Other'))
                        print(word, 'Other')
                begin_pos = end_pos + 1
                end_pos = find_next(sentence.sentence, ['.', ',', '!', '?', ':', ';', '"', '“', '”', ' '], begin_pos)
