from tokenizer_tools.tagset.offset.corpus import Corpus


def test_deltion(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")
    doc = corpus[0]

    doc_block_view = doc.as_block_view()

    reserverd_block = doc_block_view[0]
    print(reserverd_block)
    del doc_block_view[0]

    print(doc.convert_to_md())


def test_append(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")

    doc = corpus[0]

    doc_block_view = doc.as_block_view()
    reserverd_block = doc_block_view[0]
    print(reserverd_block)
    del doc_block_view[0]

    doc_block_view.append(reserverd_block)

    for block in doc_block_view:
        print(repr(block))


def test_block_view_insert(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")
    doc = corpus[0]

    doc_block_view = doc.as_block_view()

    reserverd_block = doc_block_view[0]
    print(reserverd_block)
    del doc_block_view[0]

    doc_block_view.insert(1, reserverd_block)


def test_block_view_replace(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")
    doc = corpus[0]

    doc_block_view = doc.as_block_view()

    reserverd_block = doc_block_view[0]
    print(reserverd_block)
    del doc_block_view[0]

    doc_block_view[1] = reserverd_block

    print(doc.convert_to_md())


def test_block_view_pre_and_post(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")
    doc = corpus[0]

    doc_block_view = doc.as_block_view()

    block = doc_block_view[1]

    assert block.pre == doc_block_view[0]
    assert block.post == doc_block_view[2]


def test_block_view_preceding_and_following(datadir):
    corpus = Corpus.read_from_file(datadir / "output.conllx")
    doc = corpus[0]

    doc_block_view = doc.as_block_view()

    block = doc_block_view[1]

    assert len(block.preceding) == 1
    assert len(block.following) == 6
