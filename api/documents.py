from django_elasticsearch_dsl import (fields, Index, Document)
from django_elasticsearch_dsl.registries import registry
from channels_backend.models import ElasticSearchModel

PUBLISHER_INDEX = Index("my_table")
# PUBLISHER_INDEX.settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 1
#         }

PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

@PUBLISHER_INDEX.doc_type
class NewDocument(Document):
    id = fields.IntegerField(attr="id")
    title = fields.TextField(fields = {"raw": {"type": "keyword"}})
    content = fields.TextField(fields = {"raw": {"type": "keyword"}})
    
    class Django(object):
        model = ElasticSearchModel