import collections

from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document


def find_all(string, sub):
    result = []

    sub_length = len(sub)
    start = 0
    while True:
        idx = string.find(sub, start)
        if idx == -1:
            break

        end = idx + sub_length
        result.append((idx, end))
        start = end

    return result


class ContextFreeSpan:
    def __init__(self, value=None, entity=None):
        super().__init__()

        self.value = value
        self.entity = entity


class EntityDisagreementRecord:
    def __init__(self, doc: Document = None):
        super().__init__()

        self.doc = doc
        self.groups = collections.defaultdict(list)

    def set_doc(self, doc: Document) -> "EntityDisagreementRecord":
        self.doc = doc
        return self


class EntityDisagreement:
    def __init__(self, corpus: Corpus):
        self.corpus = corpus
        self.disagreement_records = collections.defaultdict(EntityDisagreementRecord)

    def find_disagreement(self):
        entities = set()
        for doc in self.corpus:
            for span in doc.span_set:
                entities.add((span.entity, "".join(span.value)))

        for entity_type, entity_text in entities:
            self.check_entity(entity_text, entity_type)

    def check_entity(self, entity_text: str, entity_type: str):
        for doc in self.corpus:
            text = "".join(doc.text)
            sub_slices = find_all(text, entity_text)
            if not sub_slices:
                # have no relationship with the entity
                continue

            for start, end in sub_slices:
                # get entity in region
                entities = doc.get_entities_by_range(start, end)

                if not entities or len(entities) > 1:
                    self.disagreement_records[doc].set_doc(doc).groups[
                        (entity_text, entity_type)
                    ].append((start, end))
                elif (
                    "".join(entities[0].value) != entity_text
                    or entities[0].entity != entity_type
                ):
                    self.disagreement_records[doc].set_doc(doc).groups[
                        (entity_text, entity_type)
                    ].append((start, end))
