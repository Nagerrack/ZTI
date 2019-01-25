import nltk
from nltk.tag.stanford import StanfordNERTagger

from prepare_dataset import create_and_save_dataset

create_and_save_dataset('zti_corpus_test.tsv')
# sparql_queries.getTypesByUrl('http://dbpedia.org/resource/Robert_Bosch_GmbH')
list_of_enities = []


def use_tagger(text):
    nltk.internals.config_java('C:/Program Files/Java/jdk1.8.0_191/bin/java.exe')

    jar = 'stanford-ner-tagger/stanford-ner.jar'
    model = 'stanford-ner-tagger/dummy-ner-model-zti10.ser.gz'

    # Prepare NER tagger with english model
    ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

    # Tokenize: Split sentence into words
    words = nltk.word_tokenize(text)

    # Run NER tagger on words
    print(ner_tagger.tag(words))
