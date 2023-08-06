import json
from typing import Union

from tokenizer_tools.tagset.offset.corpus import Corpus


class CorpusToRasaJson:
    def __init__(self, corpus: Union[Corpus, None] = None):
        self.corpus = corpus  # type: Corpus

    @classmethod
    def read_from_file(cls, corpus_file):
        corpus = Corpus.read_from_file(corpus_file)
        self = cls(corpus)

        return self

    def convert_to_file(self, output_file):
        json_data = self.convert_to_json()

        with open(output_file, "wt") as fd:
            json.dump(json_data, fd, ensure_ascii=False)

    def convert_to_json(self):
        rasa_data = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

        common_examples = rasa_data["rasa_nlu_data"]["common_examples"]

        for offset_data in self.corpus:
            entities = []
            for i in offset_data.span_set:
                entity = {
                    "start": i.start,
                    "end": i.end,
                    "entity": i.entity,
                }
                if i.role is not None:
                    entity["role"] = i.role
                if i.group is not None:
                    entity["group"] = i.group
                entities.append(entity)

            data_item = {
                "text": "".join(offset_data.text),
                "intent": offset_data.intent,
                "entities": entities
            }

            common_examples.append(data_item)

        return rasa_data
