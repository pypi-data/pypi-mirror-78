import pytest

from tokenizer_tools.tagset.offset.transform import text_to_lower


@pytest.fixture
def doc_sample():
    from tokenizer_tools.tagset.offset.document import Document

    doc = Document.from_markdown("打开 bilibili APP")
    return doc


def test_text_to_lower(doc_sample):
    text_to_lower(doc_sample)

    assert doc_sample.text == list("打开 bilibili app")
