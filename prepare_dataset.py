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
    db_types = get_types_by_url(url)
    mutual_types = set(types).intersection(db_types)
    if not len(mutual_types) > 0:
        entity_type = mutual_types.pop()
    else:
        entity_type = 'Not_found'
    return entity_type


def create_and_save_dataset(corpus_name):
    g = rd.Graph()
    g.parse(r'oke17task2Training.xml.ttl', format='turtle')
    sentences = graph_to_train_samples(g)
    with open(corpus_name, 'w', encoding='utf-8') as corpus_file:
        for sentence in sentences:
            beginPos = 0
            endPos = sentence.sentence.find(" ")
            while endPos != -1:
                word = sentence.sentence[beginPos:endPos]
                for sign in ['.', ',', '!', '?', ':', ';', '"']:
                    word = word.replace(sign, '')
                isEntity = 0
                for entity in sentence.associated_entities:
                    if beginPos >= entity[2] and endPos <= entity[3]:
                        isEntity = 1
                        # entity_type = get_type_from_db(entity[1])
                        corpus_file.write('{0}\t{1}\n'.format(word, entity[1]))
                        print(word, entity[1])
                        break
                if isEntity == 0:
                    corpus_file.write('{0}\t{1}\n'.format(word, 'Other'))
                    print(word, 'Other')
                beginPos = endPos + 1
                endPos = sentence.sentence.find(" ", beginPos)
