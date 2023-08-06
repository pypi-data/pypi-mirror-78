import copy
from tokenizer_tools.tagset.offset.document import Document


def text_to_lower(doc: Document) -> None:
    doc.text = list(map(lambda x: x.lower(), doc.text))
