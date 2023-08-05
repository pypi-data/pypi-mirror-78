import base64
import json
import numpy as np

dfloat32 = np.dtype('>f4')


class DocumentEmbedding():
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, item_type, item, return_sequences=False):
        """
        Retrieve Embedding information.

        Args:
            item_type:             <string>
                                   item_type
            item:                  <object>
                                   item
            return_sequences:      <boolean>
                                   return_sequences
        Returns
            Embedding information

        """
        payload = {
            "item_type": item_type,
            "item": json.dumps(item),
            "return_sequences": return_sequences
        }
        response = self.client.post('document/embedding', json=payload)
        embeddings_reponse = response.json().get('embedding')
        embeddings_decoded = base64.b64decode(embeddings_reponse)
        embeddings = np.frombuffer(embeddings_decoded, dtype=dfloat32)

        return {"embedding": np.reshape(embeddings, (-1, 1024)).tolist()}
