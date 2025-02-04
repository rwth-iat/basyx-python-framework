import unittest
from fastapi.testclient import TestClient

from api.server import app

client = TestClient(app)
BASE_URL = "/api/v3.0/"

class TestFastAPIEndpoints(unittest.TestCase):

    test_submodel = {
            "id": "urn:x-test:submodel1",
            "submodelElements": [
                {
                    "idShort": "some_property",
                    "valueType": "xs:int",
                    "value": "1984",
                    "modelType": "Property"
                },
                {
                    "idShort": "some_blob",
                    "value": "3q2+7w==",
                    "contentType": "application/octet-stream",
                    "modelType": "Blob"
                },
                {
                    "idShort": "ExampleSubmodelList",
                    "typeValueListElement": "SubmodelElementList",
                    "value": [
                        {
                            "idShort": "list_1",
                            "value": "3q2+7w==",
                            "contentType": "application/octet-stream",
                            "modelType": "Blob"
                        },
                        {
                            "idShort": "list_2",
                            "value": "3q2+7w==",
                            "contentType": "application/octet-stream",
                            "modelType": "Blob"
                        }
                    ],
                    "modelType": "SubmodelElementList"
                }
            ],
            "modelType": "Submodel"
        }
    test_submodel_modified = {
            "id": "urn:x-test:submodel1",
            "submodelElements": [
                {
                    "idShort": "some_property",
                    "valueType": "xs:int",
                    "value": "8419",
                    "modelType": "Property"
                },
                {
                    "idShort": "some_blob",
                    "value": "3q2+7w==",
                    "contentType": "application/octet-stream",
                    "modelType": "Blob"
                },
                {
                    "idShort": "ExampleSubmodelList",
                    "typeValueListElement": "SubmodelElementList",
                    "value": [
                        {
                            "idShort": "list_1",
                            "value": "481563",
                            "contentType": "application/octet-stream",
                            "modelType": "Blob"
                        },
                        {
                            "idShort": "list_2",
                            "value": "&/6453=(",
                            "contentType": "application/octet-stream",
                            "modelType": "Blob"
                        }
                    ],
                    "modelType": "SubmodelElementList"
                }
            ],
            "modelType": "Submodel"
        }
    test_submode_id = test_submodel["id"]
    invalid_submode_id = "some_blob"

    def test_01_(self):
        # Test the GET /items/{item_id} endpoint
        response = client.get(BASE_URL + "submodels/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_02_post_submodel(self):
        response = client.post(BASE_URL + "submodels/", json=self.test_submodel)
        self.assertEqual(response.status_code, 200)

    def test_03_get_submodel_undefined(self):
        response_test_undefined = client.get(BASE_URL + "submodels/" + self.invalid_submode_id + "/")
        self.assertEqual(response_test_undefined.status_code, 404)

    def test_04_get_submodel(self):
        response_test_entry = client.get(BASE_URL + "submodels/" + self.test_submode_id + "/")
        self.assertEqual(response_test_entry.status_code, 200)
        self.assertEqual(response_test_entry.json(), self.test_submodel)

    def test_05_get_submodel_element(self):
        response = client.get(BASE_URL + "submodels/" + self.test_submode_id + "/submodel-elements/" + "list_1")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
