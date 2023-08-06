from datetime import datetime
from tqdm import tqdm
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from micro_toolkit.data_process.batch_iterator import BatchingIterator
from tokenizer_tools.tagset.offset.corpus import Corpus


class Doc(Document):
    md = Text(analyzer="whitespace", fields={"raw": Keyword()})
    uuid = Text(analyzer="whitespace")

    class Index:
        name = "docs"
        settings = {"number_of_shards": 1}

    @classmethod
    def bulk_save(cls, client, dicts):
        objects = (cls(**d).to_dict(include_meta=True) for d in dicts)
        return bulk(client, objects)


def insert_corpus_into_es(corpus):
    # create the mappings in elasticsearch
    Doc.init()

    batch_iterator = BatchingIterator(10000)
    client = connections.get_connection()

    def save_corpus(corpus):
        for batched_docs in tqdm(batch_iterator(corpus)):
            doc_dicts = [{"md": " ".join(doc.convert_to_md()), "uuid":doc.id} for doc in batched_docs]
            Doc.bulk_save(client, doc_dicts)

    if isinstance(corpus, Corpus):
        save_corpus(corpus)
    else:
        with Corpus.stream_reader(corpus) as corpus:
            save_corpus(corpus)


if __name__ == "__main__":
    # Define a default Elasticsearch client
    connections.create_connection(hosts=["localhost"])

    # create the mappings in elasticsearch
    Doc.init()

    insert_corpus_into_es("/home/howl/workshop/ecarx_ner_data/corpus.conllx")

    # # create and save and article
    # doc = Doc(meta={"id": 42}, md="<PERSON> 在 <GPE> 的 <ORG> 读 书 。", uuid="AAAA")
    # doc.save()

    # doc = Doc(meta={"id": 43}, md="<PERSON> 读 书 。", uuid="BBBB")
    # doc.save()

    # doc = Doc.get(id=42)
    # print(doc.uuid)

    # Display cluster health
    print(connections.get_connection().cluster.health())
