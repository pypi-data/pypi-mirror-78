from looqbox.objects.looq_object import LooqObject
import json
from collections import OrderedDict

class ObjQuery(LooqObject):

    def __init__(self, queries):
        super().__init__()
        self.queries = queries

    @property
    def to_json_structure(self):

        json_content = OrderedDict(
            {
                "objectType": "query",
                "queries": self.queries
            }
        )

        #[
        #    {"query":...., "time": 421}
        #]

        # Transforming in JSON
        list_json = json.dumps(json_content, indent=1)

        return list_json
