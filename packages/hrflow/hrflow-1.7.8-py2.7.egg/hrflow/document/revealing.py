class DocumentRevealing():
    """Manage revealing related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, text):
        """
        Retrieve Parsing information.

        Args:
            text:                   <string>
                                    text
        Returns
            Revealing information

        """
        payload = {
            "text": text
        }
        print(text)
        response = self.client.post('document/revealing', json=payload)
        return response.json()
