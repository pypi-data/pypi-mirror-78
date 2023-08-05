class Credential(object):

    headers = None
    query_params = None

    def get_headers(self):
        return self.headers or {}

    def get_query_params(self):
        return self.query_params or {}
