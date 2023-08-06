from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document


def test_attr_access(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")
    doc = corpus[0]

    assert doc.domain == "domain"
    assert doc.function == "function"
    assert doc.intent == "intent"
    assert doc.sub_function == "sub_function"


def test_attr_change(datadir, tmpdir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")
    doc = corpus[0]

    # change attr
    doc.domain = "DOMAIN"
    doc.function = "FUNCTION"
    doc.intent = "INTENT"
    doc.sub_function = "SUB_FUNCTION"

    # write out
    output_file = tmpdir / "data.conllx"
    corpus.write_to_file(output_file)

    # read in
    check_corpus = Corpus.read_from_file(output_file)
    check_doc = check_corpus[0]

    # check
    assert check_doc.domain == "DOMAIN"
    assert check_doc.function == "FUNCTION"
    assert check_doc.intent == "INTENT"
    assert check_doc.sub_function == "SUB_FUNCTION"


def test_as_string(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")
    doc = corpus[0]

    doc_string = str(doc)

    expected_doc_string = (
        "<D: domain, F: function, S: sub_function, I: intent>"
        "    "
        "[王小明](PERSON)在[北京](GPE)的[清华大学](ORG)读书。"
    )

    assert doc_string == expected_doc_string

def test_get_entities_by_range(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")

    # [王小明](PERSON)在[北京](GPE)的[清华大学](ORG)读书。
    doc = corpus[0]

    entities = doc.get_entities_by_range(0, 3)
    assert len(entities) == 1
    assert entities[0].entity == "PERSON"

    entities = doc.get_entities_by_range(0, 4)
    assert len(entities) == 1
    assert entities[0].entity == "PERSON"

    entities = doc.get_entities_by_range(0, 1)
    assert len(entities) == 1
    assert entities[0].entity == "PERSON"

    entities = doc.get_entities_by_range(2, 4)
    assert len(entities) == 1
    assert entities[0].entity == "PERSON"

    entities = doc.get_entities_by_range(2, 5)
    assert len(entities) == 2
    assert entities[0].entity == "PERSON"
    assert entities[1].entity == "GPE"

    entities = doc.get_entities_by_range(11, 12)
    assert len(entities) == 0


def test_from_markdown():
    md = "[明天](日期)的天气"
    doc = Document.from_markdown(md)
    assert doc.convert_to_md() == md

    md = "请问[明天](日期)的天气？"
    doc = Document.from_markdown(md)
    assert doc.convert_to_md() == md

    md = "请问[明天](日期)[上海](城市)的天气？"
    doc = Document.from_markdown(md)
    assert doc.convert_to_md() == md
