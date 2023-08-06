from tokenizer_tools.tagset.offset.corpus import Corpus

from tokenizer_tools.tagset.offset.diagnose.entity_disagreement import (
    EntityDisagreement,
)


def test_entity_check(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")

    ed = EntityDisagreement(corpus)
    ed.check_entity("清华大学", "NOT_ORG")
    assert len(ed.disagreement_records) == 2

    ed = EntityDisagreement(corpus)
    ed.check_entity("清华", "PART_ORG")
    assert len(ed.disagreement_records) == 2

    ed = EntityDisagreement(corpus)
    ed.check_entity("读书", "SOME_ENTITY")
    assert len(ed.disagreement_records) == 2

    ed = EntityDisagreement(corpus)
    ed.check_entity("清华大学", "ORG")
    assert len(ed.disagreement_records) == 0

def test_find_disaggrement(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    ed = EntityDisagreement(corpus)
    ed.find_disagreement()
    assert len(ed.disagreement_records) == 2
