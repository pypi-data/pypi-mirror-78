import typing
from typing import List

if typing.TYPE_CHECKING:
    from tokenizer_tools.tagset.offset.document import Document

class DocumentBlockView:
    def __init__(self, host: "Document" = None):
        self.view = None
        self.host = host
        self._build_view()

    def __delitem__(self, key):
        item = self.view[key]

        if isinstance(item, TokenBlock):
            doc_length = len(self.host.text)
            del self.host.text[item.index]
            for span in self.host.get_entities_by_range(item.index, doc_length):
                span.start -= 1
                span.end -= 1

        elif isinstance(item, SpanBlock):
            doc_length = len(self.host.text)
            for span in self.host.get_entities_by_range(item.end, doc_length):
                span.start -= item.size
                span.end -= item.size

            # import pdb; pdb.set_trace()

            for i, span in enumerate(self.host.span_set):
                if span.start == item.start and span.end == item.end:
                    del self.host.span_set[i]
                    break

            # trick: correctly delete range of text
            for _ in range(item.size):
                del self.host.text[item.start]

        self.host._notify_block_view()

    def __getitem__(self, key):
        return self.view[key]

    def __setitem__(self, key, value):
        del self[key]
        self.insert(key, value)

    def _build_view(self):
        host = self.host

        self.view = [TokenBlock(token, i) for i, token in enumerate(host.text)]
        view = self.view

        for span in reversed(host.span_set.sort_by_location()):
            blocks = view[span.start : span.end]
            sb = SpanBlock(blocks, span.start, span.end, span.entity)
            view[span.start : span.end] = [sb]

        self._compute_possion()

    def __iter__(self):
        return iter(self.view)

    def _compute_possion(self):
        pre_block = None
        for i, block in enumerate(self):
            if pre_block is not None:
                pre_block.post = block
                block.pre = pre_block

            block.preceding = self[:i]
            block.following = self[i + 1 :]

            pre_block = block

    def _notify(self):
        self._build_view()

    def append(self, value):
        from tokenizer_tools.tagset.offset.span import Span

        doc_length = len(self.host.text)

        if isinstance(value, TokenBlock):
            self.host.text.append(value.token)
        elif isinstance(value, SpanBlock):
            for t in value.tokens:
                self.host.text.append(t.token)

            span = Span(doc_length, doc_length + value.size, value.entity)
            self.host.span_set.append(span)

        self.host._notify_block_view()

    def insert(self, index, value):
        from tokenizer_tools.tagset.offset.span import Span

        doc_length = len(self.host.text)

        if isinstance(value, TokenBlock):
            self.host.text.insert(index, value.token)

            for span in self.host.get_entities_by_range(index, doc_length):
                span.start += value.size
                span.end += value.size

        elif isinstance(value, SpanBlock):
            for t in reversed(value.tokens):
                self.host.text.insert(index, t.token)

            for span in self.host.get_entities_by_range(index, doc_length):
                span.start += value.size
                span.end += value.size

            span = Span(index, index + value.size, value.entity)
            self.host.span_set.append(span)

        self.host._notify_block_view()

    def remove(self, x):
        raise NotImplementedError()

    def pop(self, x=None):
        raise NotImplementedError()

    def reverse(self):
        raise NotImplementedError()


class Block:
    pass


class TokenBlock(Block):
    def __init__(
        self,
        token=None,
        index=None,
        pre=None,
        post=None,
        preceding=None,
        following=None,
    ):
        self.token = token
        self.index = index
        self.pre = pre
        self.post = post
        self.preceding = preceding
        self.following = following
        super().__init__()

    def __str__(self):
        return f"{self.__class__.__name__}<{self.index}#{self.token}>"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"token={self.token}, "
            f"index={self.index}, "
            f"pre={self.pre}, "
            f"post={self.post}"
        )

    @property
    def size(self) -> int:
        return 1


class SpanBlock(Block):
    def __init__(
        self,
        tokens: List[TokenBlock] = None,
        start: int = None,
        end: int = None,
        entity: str = None,
        pre: TokenBlock = None,
        post: TokenBlock = None,
        preceding=None,
        following=None,
    ):
        self.tokens = tokens
        self.start = start
        self.end = end
        self.entity = entity
        self.pre = pre
        self.post = post
        self.preceding = preceding
        self.following = following
        super().__init__()

    def __str__(self):
        return "{}<{}>".format(self.__class__.__name__, [t.token for t in self.tokens])

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"tokens={self.tokens}, "
            f"start={self.start}, "
            f"end={self.end}), "
            f"entity={self.entity}, "
            f"pre={self.pre}, "
            f"post={self.post})"
        )

    @property
    def size(self) -> int:
        return self.end - self.start
