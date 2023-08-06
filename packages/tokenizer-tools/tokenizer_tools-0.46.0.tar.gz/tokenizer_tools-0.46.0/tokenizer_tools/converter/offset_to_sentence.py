from tokenizer_tools.tagset.converter.offset_to_biluo import offset_to_biluo
from tokenizer_tools.conllz.sentence import SentenceX


def offset_to_sentence(sequence):
    encoding, role, group = offset_to_biluo(sequence)  # may raise AssertionError

    if len(set(role)) == 1 and len(set(group)) == 1:
        attr_lines = [encoding]
    else:
        attr_lines = [encoding, role, group]

    sentence = SentenceX(word_lines=sequence.text, attribute_lines=attr_lines, id=sequence.id)
    sentence.meta = {'label': sequence.label}
    sentence.meta.update(sequence.extra_attr)

    return sentence
