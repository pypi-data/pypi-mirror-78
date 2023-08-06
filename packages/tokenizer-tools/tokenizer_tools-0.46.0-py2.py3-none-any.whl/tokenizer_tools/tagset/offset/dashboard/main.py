import tempfile
import argparse
import os
from collections import Counter, defaultdict, OrderedDict
from contextlib import contextmanager


from flask import Flask, request, render_template, jsonify as raw_jsonify

from tokenizer_tools.tagset.offset.analysis.document_pattern import DocumentPattern
from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.dashboard.es_create import insert_corpus_into_es
from tokenizer_tools.tagset.offset.dashboard.es_query import query_docs
from elasticsearch_dsl.connections import connections

es_query_func = {}
es_insert_func = {}

app = Flask(__name__)


class SelfIncreaser:
    def __init__(self):
        self.data = 0

    def print_self(self):
        import datetime

        print("{}: {}".format(datetime.datetime.now(), self.data))
        self.data += 1


i = SelfIncreaser()


@contextmanager
def temp_file_context(f):
    _, actual_tmp_file = tempfile.mkstemp()
    f.save(actual_tmp_file)
    yield actual_tmp_file
    os.unlink(actual_tmp_file)


class CorpusDataManager:
    def __init__(self):
        self.corpus = None
        self.corpus_docs_length = None
        self.corpus_docs_length_distribution = None
        self.corpus_docs_by_length = defaultdict(list)
        self.corpus_docs_by_token = defaultdict(list)
        self.corpus_entity_length = None
        self.corpus_docs_tokens = None
        self.corpus_statistics = None
        self.domain = None
        self.entity = None
        self.domain_corpus = None
        self.domain_corpus_statistics = None
        self.domain_pattern = None
        self.corpus_pattern = None
        self.corpus_pattern_dict = dict()
        self.domain_span_corpus = defaultdict(lambda: defaultdict(list))
        self.entity_corpus = defaultdict(list)
        self.domain_entity_corpus = defaultdict(lambda: defaultdict(list))
        self.domain_entity_span_corpus = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )
        self.span_corpus = defaultdict(list)
        self.span_entity_corpus = defaultdict(lambda: defaultdict(list))
        self.failure_analysis = defaultdict(
            lambda: [None, None, None, None, None, None]
        )

    def build_from_corpus_file(self, corpus_file):
        i.print_self()

        self.corpus = Corpus.read_from_file(corpus_file)
        i.print_self()

        self.corpus_statistics = self.corpus.generate_statistics()
        i.print_self()

        self.domain = list(dict(self.corpus_statistics.domain.most_common()).keys())
        i.print_self()

        self.entity = list(
            dict(self.corpus_statistics.entity_count.most_common()).keys()
        )
        i.print_self()

        domain_doc_list = defaultdict(list)
        for doc in self.corpus:
            domain_doc_list[doc.domain].append(doc)
        self.domain_corpus = {k: Corpus(v) for k, v in domain_doc_list.items()}
        i.print_self()

        self.domain_corpus_statistics = {
            k: v.generate_statistics() for k, v in self.domain_corpus.items()
        }
        i.print_self()

        self.corpus_pattern = self.corpus.generate_pattern()
        i.print_self()

        for pattern in self.corpus_pattern:
            self.corpus_pattern_dict[pattern.convert_to_md()] = pattern
        i.print_self()

        for domain_name, stat in self.domain_corpus_statistics.items():
            target_corpus = corpus_data_manager.domain_corpus[domain_name]
            for entity_type in stat.entity_types.keys():
                data = []
                for doc in target_corpus:
                    for span in doc.span_set:
                        if span.entity == entity_type:
                            data.append(doc)
                            break
                self.domain_entity_corpus[domain_name][entity_type] = data
        i.print_self()

        for domain_name, stat in self.domain_corpus_statistics.items():
            for entity_type in stat.entity_types.keys():
                target_corpus = self.domain_entity_corpus[domain_name][entity_type]
                # span_values = {
                #     tuple(span.value) for doc in target_corpus for span in doc.span_set
                # }
                # for span_value in span_values:
                #     data = []
                #     for doc in target_corpus:
                #         for span in doc.span_set:
                #             if (
                #                 tuple(span.value) == span_value
                #                 and span.entity == entity_type
                #             ):
                #                 data.append(doc)
                #                 break
                #     self.domain_entity_span_corpus[domain_name][entity_type][
                #         span_value
                #     ] = data
                for doc in target_corpus:
                    for span in doc.span_set:
                        if span.entity == entity_type:
                            span_value = tuple(span.value)
                            self.domain_entity_span_corpus[domain_name][entity_type][
                                span_value
                            ].append(doc)
        i.print_self()

        for domain_name, stat in self.domain_corpus_statistics.items():
            # for span_value in stat.entity_values.keys():
            #     data = []
            #     for doc in self.domain_corpus[domain_name]:
            #         for span in doc.span_set:
            #             if tuple(span.value) == span_value:
            #                 data.append(doc)
            #                 break
            #     self.domain_span_corpus[domain_name][span_value] = data
            for doc in self.domain_corpus[domain_name]:
                for span in doc.span_set:
                    span_value = tuple(span.value)
                    self.domain_span_corpus[domain_name][span_value].append(doc)
        i.print_self()

        # for span_value in self.corpus_statistics.entity_values.keys():
        #     for entity_type in self.corpus_statistics.entity_types.keys():
        #         data = []
        #         for doc in corpus_data_manager.corpus:
        #             for span in doc.span_set:
        #                 if (
        #                     tuple(span.value) == span_value
        #                     and span.entity == entity_type
        #                 ):
        #                     data.append(doc)
        #                     break
        #         self.span_entity_corpus[span_value][entity_type] = data
        for doc in self.corpus:
            for span in doc.span_set:
                span_value = tuple(span.value)
                entity_type = span.entity
                self.span_entity_corpus[span_value][entity_type].append(doc)
        i.print_self()

        # for entity_type in self.corpus_statistics.entity_types.keys():
        #     data = []
        #     for doc in self.corpus:
        #         for span in doc.span_set:
        #             if span.entity == entity_type:
        #                 data.append(doc)
        #                 break
        #     self.entity_corpus[entity_type] = data
        for doc in self.corpus:
            for span in doc.span_set:
                entity_type = span.entity
                self.entity_corpus[entity_type].append(doc)
        i.print_self()

        docs_es_insert_func = es_insert_func.get("docs")
        if docs_es_insert_func:
            docs_es_insert_func(self.corpus)
        i.print_self()

        # for span_value in self.corpus_statistics.entity_values.keys():
        #     data = []
        #     for doc in self.corpus:
        #         for span in doc.span_set:
        #             if tuple(span.value) == span_value:
        #                 data.append(doc)
        #                 break
        #     self.span_corpus[span_value] = data
        for doc in self.corpus:
            for span in doc.span_set:
                span_value = tuple(span.value)
                self.span_corpus[span_value].append(doc)
        i.print_self()

        docs_length = []
        for doc in self.corpus:
            doc_len = len(doc.text)
            docs_length.append(doc_len)
            self.corpus_docs_by_length[doc_len].append(doc)
        distribution = Distribution(Counter(docs_length))
        self.corpus_docs_length = distribution.kv_data
        self.corpus_docs_length_distribution = distribution.precentile
        i.print_self()

        entity_length = []
        for doc in self.corpus:
            for span in doc.span_set:
                entity_length.append(len(span.entity))
        distribution = Distribution(Counter(entity_length))
        self.corpus_entity_length = distribution.kv_data
        i.print_self()

        docs_tokens = []
        for doc in self.corpus:
            docs_tokens.extend(doc.text)
            for token in doc.text:
                self.corpus_docs_by_token[token].append(doc)
        self.corpus_docs_tokens = Counter(docs_tokens)
        i.print_self()

    def build_from_failure_analysis(self, actual_file, expected_file):
        for doc in Corpus.read_from_file(actual_file):
            self.failure_analysis[doc.id][0] = doc
            self.failure_analysis[doc.id][2] = (
                DocumentPattern.build_from_document(doc).convert_to_md()
                in self.corpus_pattern_dict
            )
            self.failure_analysis[doc.id][4] = any(
                [
                    tuple(span.value)
                    in self.corpus_statistics.entity_types.get(span.entity, [])
                    for span in doc.span_set
                ]
            )

        for doc in Corpus.read_from_file(expected_file):
            self.failure_analysis[doc.id][1] = doc
            self.failure_analysis[doc.id][3] = (
                DocumentPattern.build_from_document(doc).convert_to_md()
                in self.corpus_pattern_dict
            )
            self.failure_analysis[doc.id][5] = any(
                [
                    tuple(span.value)
                    in self.corpus_statistics.entity_types.get(span.entity, [])
                    for span in doc.span_set
                ]
            )


corpus_data_manager = CorpusDataManager()


class FailureAnalysisDataManager:
    def __init__(self):
        pass

    def build(self, actual, expected):
        pass


class InspectorDataManager:
    def __init__(self):
        pass

    def build(self, corpus):
        pass


class Distribution:
    def __init__(self, data: Counter):
        self.data = data

        self.kv_data = self.build_kv()
        self.precentile = self.build_precentile()

    def build_kv(self):
        raw_data = dict(self.data.most_common())
        max_v = max(k for k, v in self.data.most_common())

        data = OrderedDict()
        for i in range(1, max_v + 1):
            data[i] = raw_data.get(i, 0)

        return data

    def build_precentile(self):
        import numpy as np

        np_data = np.array(list(self.data.elements()), dtype=np.int32)
        print(np_data)
        p80 = np.percentile(np_data, 80)
        p85 = np.percentile(np_data, 85)
        p90 = np.percentile(np_data, 90)
        p95 = np.percentile(np_data, 95)
        p96 = np.percentile(np_data, 96)
        p97 = np.percentile(np_data, 97)
        p98 = np.percentile(np_data, 98)
        p99 = np.percentile(np_data, 99)
        mean = np.mean(np_data)
        median = np.median(np_data)

        return [mean, median, p80, p85, p90, p95, p96, p97, p98, p99]


def jsonify(data):
    if isinstance(data, Counter):
        data = dict(data.most_common())

        return raw_jsonify(
            {"categories": list(data.keys()), "data": list(data.values())}
        )
    elif isinstance(data, dict):
        return raw_jsonify(
            {"categories": list(data.keys()), "data": list(data.values())}
        )

    raise ValueError(data)


def render_table(request_args, data, date_type=None):
    total_data_len = len(data)
    draw = request_args.get("draw")
    start = int(request_args.get("start"))
    length = int(request_args.get("length"))
    pattern = request_args.get("search[value]")

    print(pattern)

    working_data = None
    if pattern:
        if date_type is not None and es_query_func.get(date_type):
            print("using ES")
            query_func = es_query_func.get(date_type)
            _, working_id = query_func(pattern)
            working_data = [data.get_doc_by_id(i) for i in working_id]
        else:
            print("Using builtin")
            working_data = [i[0] for i in data.fuzzy_search(pattern, 10)]
    else:
        working_data = data

    filtered_data_len = len(working_data)

    end = start + length
    data_piece = working_data[start:end]

    return raw_jsonify(
        {
            "draw": draw,
            "recordsTotal": total_data_len,
            "recordsFiltered": filtered_data_len,
            "data": [[doc.domain, doc.convert_to_md()] for doc in data_piece],
        }
    )


def render_failure_table(request_args, data):
    data_len = len(data)
    draw = request_args.get("draw")
    start = int(request_args.get("start"))
    length = int(request_args.get("length"))

    end = start + length

    data_piece = list(data.values())[start:end]

    return raw_jsonify(
        {
            "draw": draw,
            "recordsTotal": data_len,
            "recordsFiltered": data_len,
            "data": [
                [
                    actual_doc.domain,
                    actual_doc.convert_to_md(),
                    expected_doc.domain,
                    expected_doc.convert_to_md(),
                    actual_pattern_in,
                    expected_pattern_in,
                    actual_entity_in,
                    expected_entity_in,
                ]
                for actual_doc, expected_doc, actual_pattern_in, expected_pattern_in, actual_entity_in, expected_entity_in in data_piece
            ],
        }
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/corpus", methods=["GET"])
def page_of_corpus():
    return render_template("corpus.html")


@app.route("/failure", methods=["GET"])
def page_of_failure():
    return render_template("failure.html")


@app.route("/failure/docs", methods=["GET"])
def docs_of_failure():
    return render_failure_table(request.args, corpus_data_manager.failure_analysis)


@app.route("/failure", methods=["POST"])
def data_of_failure():
    actual = request.files["actual"]
    expected = request.files["expected"]

    if (
        actual is None
        or actual.filename == ""
        or expected is None
        or expected.filename == ""
    ):
        raise ValueError()
    if actual:
        with temp_file_context(actual) as actual_tmp_file, temp_file_context(
            expected
        ) as expected_tmp_file:
            corpus_data_manager.build_from_failure_analysis(
                actual_tmp_file, expected_tmp_file
            )

        return "OK"


@app.route("/corpus", methods=["POST"])
def upload_corpus():
    f = request.files.get("file", None)
    if f is None or f.filename == "":
        raise ValueError()
    if f:
        with temp_file_context(f) as tmp_file:
            corpus_data_manager.build_from_corpus_file(tmp_file)

        return "OK"


@app.route("/corpus/docs", methods=["GET"])
def get_docs():
    return render_table(request.args, corpus_data_manager.corpus, "docs")


@app.route("/corpus/docs/length", methods=["GET"])
def get_docs_length():
    return jsonify(corpus_data_manager.corpus_docs_length)


@app.route("/corpus/docs/length/<int:length>", methods=["GET"])
def get_docs_by_length(length):
    return render_template("doc_length.html", docs_length=length)


@app.route("/corpus/docs/length/<int:length>/list", methods=["GET"])
def get_docs_by_length_data(length):
    return render_table(request.args, corpus_data_manager.corpus_docs_by_length[length])


@app.route("/corpus/docs/length_distribution", methods=["GET"])
def get_docs_length_distribution():
    return raw_jsonify({"data": [corpus_data_manager.corpus_docs_length_distribution]})


@app.route("/corpus/docs/tokens", methods=["GET"])
def get_docs_tokens():
    return jsonify(corpus_data_manager.corpus_docs_tokens)


@app.route("/corpus/docs/tokens/<string:token>", methods=["GET"])
def get_docs_by_token_page(token):
    return render_template("docs_by_token.html", token=token)


@app.route("/corpus/docs/tokens/<string:token>/list", methods=["GET"])
def get_docs_by_token(token):
    print("'{}'".format(token))
    return render_table(request.args, corpus_data_manager.corpus_docs_by_token[token])


@app.route("/corpus/domains", methods=["GET"])
def get_domains():
    return jsonify(corpus_data_manager.corpus_statistics.domain)


@app.route("/corpus/patterns", methods=["GET"])
def get_patterns():
    return render_table(request.args, corpus_data_manager.corpus_pattern)


@app.route("/corpus/pattern/<string:pattern_text>", methods=["GET"])
def get_pattern(pattern_text):
    return render_template("pattern.html", pattern_text=pattern_text)


@app.route("/corpus/pattern/<string:pattern_text>/docs", methods=["GET"])
def get_docs_by_pattern(pattern_text):
    data = corpus_data_manager.corpus_pattern_dict[pattern_text]

    return render_table(request.args, data.docs)


@app.route("/corpus/<string:domain_name>/docs", methods=["GET"])
def get_docs_by_domain(domain_name):
    return render_table(request.args, corpus_data_manager.domain_corpus[domain_name])


@app.route("/corpus/domains/<string:domain_name>", methods=["GET"])
def get_domain_by_id(domain_name):
    # return "domain page of {}".format(domain[domain_id])
    return render_template("domain.html", domain_name=domain_name)


@app.route("/corpus/entity_count", methods=["GET"])
def get_entity_count():
    return jsonify(corpus_data_manager.corpus_statistics.entity_count)


@app.route("/corpus/entity_length", methods=["GET"])
def get_entity_length():
    return jsonify(corpus_data_manager.corpus_entity_length)


@app.route("/corpus/entity/<string:entity_type>", methods=["GET"])
def get_entity_by_name(entity_type):
    return render_template("entity.html", entity_type=entity_type)


@app.route("/corpus/entity/<string:entity_type>/value", methods=["GET"])
def get_entity_by_type(entity_type):
    return jsonify(corpus_data_manager.corpus_statistics.entity_types[entity_type])


@app.route("/corpus/domain/<string:domain_name>/entity_count", methods=["GET"])
def get_entity_count_by_domain_id(domain_name):
    return jsonify(
        corpus_data_manager.domain_corpus_statistics[domain_name].entity_count
    )


@app.route(
    "/corpus/domain/<string:domain_name>/entity/<string:entity_type>", methods=["GET"]
)
def get_entity_by_domain_id_and_entity_type(domain_name, entity_type):
    return render_template(
        "domain_entity.html", domain_name=domain_name, entity_type=entity_type
    )


@app.route(
    "/corpus/domain/<string:domain_name>/entity/<string:entity_type>/span/<string:span_value>",
    methods=["GET"],
)
def get_page_by_domain_and_entity_and_span(domain_name, entity_type, span_value):
    return render_template(
        "domain_entity_span.html",
        domain_name=domain_name,
        entity_type=entity_type,
        span_value=span_value,
    )


@app.route(
    "/corpus/domain/<string:domain_name>/entity/<string:entity_type>/docs",
    methods=["GET"],
)
def get_docs_by_domain_id_and_entity_type(domain_name, entity_type):
    data = corpus_data_manager.domain_entity_corpus[domain_name][entity_type]

    return render_table(request.args, data)


@app.route(
    "/corpus/domain/<string:domain_name>/entity/<string:entity_type>/span/<string:span_value>/docs",
    methods=["GET"],
)
def get_docs_by_domain_and_entity_and_span(domain_name, entity_type, span_value):
    span_value = tuple(span_value.split(","))

    data = corpus_data_manager.domain_entity_span_corpus[domain_name][entity_type][
        span_value
    ]

    return render_table(request.args, data)


@app.route(
    "/corpus/domain/<string:domain_name>/span/<string:span_value>/docs", methods=["GET"]
)
def get_docs_by_domain_id_and_span_value(domain_name, span_value):
    span_value = tuple(span_value.split(","))

    data = corpus_data_manager.domain_span_corpus[domain_name][span_value]

    return render_table(request.args, data)


@app.route(
    "/corpus/domain/<string:domain_name>/entity/<string:entity_type>/value",
    methods=["GET"],
)
def get_entity_value_by_domain_id_and_entity_type(domain_name, entity_type):
    return jsonify(
        corpus_data_manager.domain_corpus_statistics[domain_name].entity_types[
            entity_type
        ]
    )


@app.route(
    "/corpus/domain/<string:domain_name>/span/<string:span_value>", methods=["GET"]
)
def get_span_by_domain_id_and_entity_type(domain_name, span_value):
    return render_template(
        "domain_span.html", domain_name=domain_name, span_value=span_value
    )


@app.route("/corpus/span/<string:span_value>", methods=["GET"])
def get_span_by_span_value(span_value):
    return render_template("span.html", span_value=span_value)


@app.route(
    "/corpus/span/<string:span_value>/entity/<string:entity_type>", methods=["GET"]
)
def get_span_by_span_value_and_entity(span_value, entity_type):
    return render_template(
        "span_entity.html", span_value=span_value, entity_type=entity_type
    )


@app.route(
    "/corpus/span/<string:span_value>/entity/<string:entity_type>/docs", methods=["GET"]
)
def get_docs_by_span_value_and_entity_type(span_value, entity_type):
    span_value = tuple(span_value.split(","))

    data = corpus_data_manager.span_entity_corpus[span_value][entity_type]

    return render_table(request.args, data)


@app.route("/corpus/span/<string:span_value>/value", methods=["GET"])
def get_span_list_by_span_value(span_value):
    span_value = tuple(span_value.split(","))
    return jsonify(corpus_data_manager.corpus_statistics.entity_values[span_value])


@app.route(
    "/corpus/domain/<string:domain_name>/span/<string:span_value>/value",
    methods=["GET"],
)
def get_span_value_by_domain_id_and_entity_type(domain_name, span_value):
    span_value = tuple(span_value.split(","))
    return jsonify(
        corpus_data_manager.domain_corpus_statistics[domain_name].entity_values[
            span_value
        ]
    )


@app.route("/corpus/entity/<string:entity_type>/docs", methods=["GET"])
def get_docs_by_entity_type(entity_type):
    data = corpus_data_manager.entity_corpus[entity_type]

    return render_table(request.args, data)


@app.route("/corpus/span/<string:span_value>/docs", methods=["GET"])
def get_docs_by_span_value(span_value):
    span_value = tuple(span_value.split(","))

    data = corpus_data_manager.span_corpus[span_value]

    return render_table(request.args, data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use_es",
        action="store_true",
        help="Using ElasticSearch as doc search engine, default is using fuzzywuzzy",
        default=False,
        required=False,
    )

    config = vars(parser.parse_args())

    print(config)

    if config.get("use_es", False):
        connections.create_connection(hosts=["localhost"])
        es_query_func["docs"] = query_docs
        es_insert_func["docs"] = insert_corpus_into_es

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host="0.0.0.0")
