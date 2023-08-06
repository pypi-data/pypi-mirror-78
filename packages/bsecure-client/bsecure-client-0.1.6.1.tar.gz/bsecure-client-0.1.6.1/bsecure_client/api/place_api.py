from .base import API

get_tenant_query = """
  query getTenant(
    $uuid: UUID!
  ) {
    tenant(uuid: $uuid) {
      id
      uuid
      name
      place {
        id
        uuid
        name
        shortName
        description
        formattedAddress
        gcsCoord
        frontPhoto
      }
    }
  }
"""

push_tenant_query = """
  mutation pushTenant(
    $name: String!,
    $formattedAddress: String!,
    $latitude: Float!,
    $longitude: Float!,
    $clientName: String,
    $frontPhoto: String
  ) {
    pushTenant(input: {
      name: $name,
      formattedAddress: $formattedAddress,
      latitude: $latitude,
      longitude: $longitude,
      clientName: $clientName,
      frontPhoto: $frontPhoto
    }) {
      tenant {
        uuid
      }
    }
  }
"""

upload_place_front_photo_query = """
  mutation uploadPlaceFrontPhoto($filename: String!) {
    uploadPlaceFrontPhoto(input: {filename: $filename}) {
      fileId,
      presignedUrl
    }
  }
"""

create_place_document_by_tenant_query = """
  mutation createPlaceDocumentByTenant(
    $tenantUuid: UUID!,
    $title: String!,
    $fileId: String!,
    $type: String!
  ) {
    createPlaceDocumentByTenant(input: {
      tenantUuid: $tenantUuid,
      title: $title,
      fileId: $fileId,
      type: $type
    }) {
      placeDocument {
        uuid
      }
    }
  }
"""

update_place_document_query = """
  mutation updatePlaceDocument($uuid: UUID!, $title: String, $fileId: String, $type: String) {
    updatePlaceDocument(uuid: $uuid, input: {title: $title, fileId: $fileId, type: $type}) {
      placeDocument {
        uuid
      }
    }
  }
"""

upload_place_document_query = """
  mutation uploadPlaceDocument($filename: String!) {
    uploadPlaceDocument(input: {filename: $filename}) {
      fileId,
      presignedUrl
    }
  }
"""

all_place_documents_by_tenant_query = """
  query allPlaceDocumentsByTenant($tenantUuid: UUID!) {
    allPlaceDocumentsByTenant(tenantUuid: $tenantUuid) {
      edges {
        node {
          title
          filename
          type
          uploadedTimestamp
        }
      }
    }
  }
"""

all_documents_by_property_query = """
  query allDocumentsByProperty($propertyUuid: UUID!) {
    allDocumentsByProperty(propertyUuid: $propertyUuid) {
      edges {
        node {
          title
          filename
          type
          uploadedTimestamp
        }
      }
    }
  }
"""


class PlaceAPI(API):
    # TODO: Would be nice to be able to share these with the server
    # implementation.
    PUBLIC = "Public"
    AUDIT = "Audit"
    SERVICE = "Service"

    @API.expose_method
    def push_tenant(self, name, formatted_address, gcs_coord, client_name=None, front_photo=None):
        front_photo_file_id = self.upload_front_photo(front_photo)
        response_data = self.perform_query(
            push_tenant_query,
            self.make_variables(
                name=name,
                formattedAddress=formatted_address,
                longitude=gcs_coord[0],
                latitude=gcs_coord[1],
                clientName=client_name,
                frontPhoto=front_photo_file_id,
            ),
        )
        return response_data["pushTenant"]["tenant"]["uuid"]

    def upload_front_photo(self, front_photo):
        return self.upload_file(
            front_photo, upload_place_front_photo_query, "uploadPlaceFrontPhoto"
        )

    @API.expose_method
    def create_place_document_by_tenant(self, tenant_uuid, title, document, type=PUBLIC):
        document_file_id = self.upload_place_document(document)
        response_data = self.perform_query(
            create_place_document_by_tenant_query,
            {"tenantUuid": tenant_uuid, "title": title, "fileId": document_file_id, "type": type},
        )
        return response_data["createPlaceDocumentByTenant"]["placeDocument"]["uuid"]

    @API.expose_method
    def update_place_document(self, uuid, title=None, document=None, type=None):
        document_file_id = self.upload_place_document(document)
        response_data = self.perform_query(
            update_place_document_query,
            self.make_variables(uuid=uuid, title=title, fileId=document_file_id, type=type),
        )
        return response_data["updatePlaceDocument"]["placeDocument"]["uuid"]

    @API.expose_method
    def all_place_documents_by_tenant(self, tenant_uuid):
        response_data = self.perform_query(
            all_place_documents_by_tenant_query, {"tenantUuid": tenant_uuid}
        )
        return [edge["node"] for edge in response_data["allPlaceDocumentsByTenant"]["edges"]]

    @API.expose_method
    def all_documents_by_property(self, property_uuid):
        response_data = self.perform_query(
            all_documents_by_property_query, {"propertyUuid": property_uuid}
        )
        return [edge["node"] for edge in response_data["allDocumentsByProperty"]["edges"]]

    def upload_place_document(self, document):
        return self.upload_file(document, upload_place_document_query, "uploadPlaceDocument")

    @API.expose_method
    def get_tenant(self, uuid: str):
        """Returns a tenant (and parent place) by uuid"""
        response_data = self.perform_query(get_tenant_query, {"uuid": uuid})
        return response_data["tenant"]
