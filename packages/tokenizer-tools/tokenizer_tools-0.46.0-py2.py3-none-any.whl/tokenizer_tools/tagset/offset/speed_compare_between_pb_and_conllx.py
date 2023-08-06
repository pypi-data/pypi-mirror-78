from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.corpus_protobuf import dump_corpus_to_pb
import timeit

test_corpus = Corpus.read_from_file("./corpus.conllx")
dump_corpus_to_pb(test_corpus, "corpus.pb")

result = timeit.repeat(
    "load_corpus_from_pb('./corpus.pb')",
    repeat=3,
    number=1,
    setup="from tokenizer_tools.tagset.offset.corpus_protobuf import load_corpus_from_pb",
)
print(result)

result = timeit.repeat(
    "Corpus.read_from_file('./corpus.conllx')",
    repeat=3,
    number=1,
    setup="from tokenizer_tools.tagset.offset.corpus import Corpus",
)
print(result)
