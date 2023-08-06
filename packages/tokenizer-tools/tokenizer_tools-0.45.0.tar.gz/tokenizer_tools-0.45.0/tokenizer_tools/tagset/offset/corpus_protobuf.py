import mmap

from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.span_set import SpanSet
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset import corpus_pb2


def dump_corpus_to_pb(corpus: Corpus, pb_file):
    pb_corpus = corpus_pb2.Corpus()
    for doc in corpus:
        pb_doc = pb_corpus.docs.add()

        pb_doc.text.extend(doc.text)

        for span in doc.span_set:
            pb_span = pb_doc.span_set.add()
            pb_span.entity = span.entity
            pb_span.start = span.start
            pb_span.end = span.end
            pb_span.role = span.role or ""
            pb_span.group = span.group or ""

        pb_doc.meta.id = doc.id or ""
        pb_doc.meta.domain = doc.domain or ""
        pb_doc.meta.intent = doc.intent or ""

    with open(pb_file, "wb") as fd:
        fd.write(pb_corpus.SerializeToString())


def parse_corpus_from_pb(pb_corpus: corpus_pb2.Corpus) -> Corpus:
    doc_list = []
    for pb_doc in pb_corpus.docs:
        text = pb_doc.text

        span_list = []
        for pb_span in pb_doc.span_set:
            span = Span(entity=pb_span.entity, start=pb_span.start, end=pb_span.end, role=pb_span.role, group=pb_span.group)
            span_list.append(span)
        span_set = SpanSet(span_list)

        domain = pb_doc.meta.domain
        intent = pb_doc.meta.intent
        id_ = pb_doc.meta.id

        doc = Document(text=text, span_set=span_set)
        doc.intent = intent
        doc.domain = domain
        doc.id = id_

        doc_list.append(doc)

    return Corpus(doc_list)


def load_corpus_from_pb(pb_file) -> Corpus:
    pb_corpus = corpus_pb2.Corpus()

    # normal way
    # with open(pb_file, "rb") as fd:
    #     pb_corpus.ParseFromString(fd.read())

    # mmap way
    with open(pb_file, "rb") as raw_fd:
        with mmap.mmap(raw_fd.fileno(), length=0, access=mmap.ACCESS_READ) as fd:
            pb_corpus.ParseFromString(fd.read())

    return parse_corpus_from_pb(pb_corpus)


def convert_conllx_to_pb(conllx_file, pb_file):
    corpus = Corpus.read_from_file(conllx_file)
    dump_corpus_to_pb(corpus, pb_file)
