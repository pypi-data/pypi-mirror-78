import itertools
import typing

from tokenizer_tools.tagset.offset.analysis.document_pattern import DocumentPattern
from tokenizer_tools.tagset.offset.analysis.entity_placeholder import EntityPlaceholder
from tokenizer_tools.tagset.offset.span_set import SpanSet

if typing.TYPE_CHECKING:
    from tokenizer_tools.tagset.offset.analysis.corpus_pattern import CorpusPattern

def parse_plain_line(raw_text: str) -> DocumentPattern:
    text = raw_text.strip()

    placeholders = []
    tokens = []

    pattern_tokens = []
    in_pattern = False

    offset = 0
    tmp_start = None
    for i, token in enumerate(text):
        if token == "<":
            in_pattern = True
            tmp_start = offset
            continue
        if token == ">":
            offset += 1

            pattern = "".join(pattern_tokens)
            end = offset
            placeholders.append(
                EntityPlaceholder(start=tmp_start, end=end, entity=pattern)
            )
            tokens.append(pattern)

            # reset
            pattern_tokens = []
            in_pattern = False

            continue

        if in_pattern:
            pattern_tokens.append(token)
        else:
            offset += 1
            tokens.append(token)

    doc_pattern = DocumentPattern(tokens)
    doc_pattern.entities = SpanSet(placeholders)

    return doc_pattern

def parse_plain_text(raw_text: str) -> "CorpusPattern":
    from tokenizer_tools.tagset.offset.analysis.corpus_pattern import CorpusPattern

    lines = filter(lambda x: x.strip(), raw_text.split("\n"))
    docs = [parse_plain_line(line) for line in lines]

    return CorpusPattern(docs)



if __name__ == "__main__":
    result = parse_plain_line("把<座椅位置>的空调的靠上提<温度调节幅度>温度")
    print(result)
