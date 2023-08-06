import logging

from . import utils
from .utils import ParserOutputType


logging.basicConfig(
    format='%(levelname)s %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.INFO
)


class MLPProcessor:

    def __init__(self, mlp):
        self.mlp = mlp


    def apply_mlp(self, generator):
        """ Applies MLP to objects in a given generator.
        """
        for item in generator:
            item_type = utils.get_output_type(item)

            if (item_type == ParserOutputType.EMAIL):
                email, attachments = item
                self._apply_mlp_to_mails(email, attachments)

            elif (item_type == ParserOutputType.COLLECTION):
                self._apply_mlp_to_collection_item(item)
            else:
                self._apply_mlp(item, "text")

            yield item


    def _apply_mlp(self, document: dict, field: str):
        if (field not in document):
            return
        content = document.get(field, "")

        if content:
            mlp_res = self.mlp.process(content)
            mlp_res_path = field + "_mlp"
            document[mlp_res_path] = mlp_res["text"]  # Add the MLP output dictionary.

            facts = []
            for f in mlp_res["texta_facts"]:
                f["doc_path"] = f"{mlp_res_path}.text"
                facts.append(f)

            if facts:
                document["texta_facts"] = facts


    def _apply_mlp_to_mails(self, email, attachments):
        self._apply_mlp(email, "body")
        for attachment in attachments:
            self._apply_mlp(attachment, "content")


    # apply it to all fields as we don't know anything about the item or it's fields
    def _apply_mlp_to_collection_item(self, item: dict):
        item_copy = item.copy()
        for key in item_copy.keys():
            self._apply_mlp(item, key)
