from typing import List, Union

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from elasticsearch_dsl.connections import connections
from tokenizer_tools.tagset.offset.dashboard.es_create import Doc


class DocSearch(FacetedSearch):
    index = "docs"
    doc_types = [Doc]
    # fields that should be searched
    fields = ["md", "uuid"]


def query_docs(query_str: str) -> Union[object, List[int]]:
    ds = DocSearch(" ".join(query_str))
    ds = ds[:500]
    response = ds.execute()

    return response, [hit.uuid for hit in response]


if __name__ == "__main__":
    # Define a default Elasticsearch client
    connections.create_connection(hosts=["localhost"])

    response, _ = query_docs("有[游泳池](酒店设施)的酒店")

    for hit in response:
        print(hit.meta.score, hit.md, hit.uuid)
