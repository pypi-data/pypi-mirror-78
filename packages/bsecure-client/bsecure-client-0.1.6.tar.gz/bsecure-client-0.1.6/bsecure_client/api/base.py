import requests

from ..exceptions import QueryException
from ..utils import FileID, remove_trailing_slash


class API:
    SUCCESS_RESPONSE_CODES = (200, 201)

    @classmethod
    def expose_method(cls, method):
        method.expose = True
        return method

    def __init__(self, client):
        self.client = client

    def perform_query(self, query, variables=None, headers=None):
        response = self.send_query(query, variables, headers)
        response.raise_for_status()
        response_data = response.json()
        self.check_for_errors(response_data)
        return response_data["data"]

    def send_query(self, query, variables, headers):
        domain = remove_trailing_slash(self.client.domain)
        url = f"{self.client.protocol}://{domain}/graphql/"
        auth_headers = {}

        if self.client.jwt:
            auth_headers["Authorization"] = f"Bearer {self.client.jwt}"
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers={
                **({"Origin": self.client.origin} if self.client.origin else {}),
                **auth_headers,
                **(headers or {}),
            },
        )
        # This will only trigger for 400/500 django view exceptions.
        if response.status_code not in self.SUCCESS_RESPONSE_CODES:
            msg = response.content
            raise QueryException(f"BSECURE error: {msg}")

        return response

    def upload_file(self, file, upload_query, response_key):
        if not file:
            return None
        response_data = self.perform_query(upload_query, {"filename": file.filename})
        # TODO: At present the query returns uploadAssetPhoto as a key with None value only if the
        # query does not pass. This should obviously be changed to an error at some point!
        if response_key not in response_data.keys() or not response_data[response_key]:
            raise QueryException("Failed to upload file: You do not have permission")

        file_id = response_data[response_key]["fileId"]
        presigned_url = response_data[response_key]["presignedUrl"]
        upload_response = requests.put(presigned_url, data=file.content.read())
        if upload_response.status_code != 200:
            raise QueryException(f"Failed to upload file: {upload_response.text}")
        return file_id

    def check_for_errors(self, response_data):
        # GraphQL responses only throw 400s and 500s if something goes
        # very wrong, so we need to check the error fields in addition.
        if response_data.get("errors"):
            try:
                msg = response_data["errors"][0]["message"]
            except Exception:
                msg = "unknown reason"
            raise QueryException(f"BSECURE error: {msg}")

    def make_variables(self, **kwargs):
        return {key: value for key, value in kwargs.items() if value is not None}

    def check_file_id(self, file_id):
        if file_id is not None:
            if not isinstance(file_id, FileID):
                raise TypeError("File uploads must be FileID objects")
            file_id = str(file_id)
        return file_id
