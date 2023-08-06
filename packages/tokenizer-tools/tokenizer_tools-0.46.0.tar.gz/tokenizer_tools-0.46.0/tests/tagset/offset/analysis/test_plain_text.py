from tokenizer_tools.tagset.offset.analysis.plain_text import parse_plain_text

def test_parse_plain_text(datadir):
    with (datadir / "data.txt").open("rt") as fd:
        corpus_pattern = parse_plain_text(fd.read())

    print(corpus_pattern)
    assert len(corpus_pattern) == 2
