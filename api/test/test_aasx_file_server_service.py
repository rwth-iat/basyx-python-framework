import unittest
from fastapi.testclient import TestClient

from api.server import app
from .examples.aasx_packages import aasx_package
from .examples.submodels import test_submodel_modified, test_submodel

client = TestClient(app)
BASE_URL = "/api/v3.0/"


class TestFastAPIEndpoints(unittest.TestCase):
    test_submode_id = test_submodel["id"]
    invalid_submodel_id = "some_blob"

    def test_01_(self):
        # Test the GET /items/{item_id} endpoint
        response = client.get(BASE_URL + "aasx/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_02_post_aasx_package(self):

        response = client.post(BASE_URL + "aasx/", json=test_submodel)
        self.assertEqual(response.status_code, 200)

    def test_03_get_submodel_undefined(self):
        response_test_undefined = client.get(BASE_URL + "aasx/" + self.invalid_submodel_id + "/")
        self.assertEqual(response_test_undefined.status_code, 404)

    def test_04_get_submodel(self):
        response_test_entry = client.get(BASE_URL + "aasx/" + self.test_submode_id + "/")
        self.assertEqual(response_test_entry.status_code, 200)
        self.assertEqual(response_test_entry.json(), test_submodel)

    def test_05_get_submodel_element(self):
        response = client.get(BASE_URL + "aasx/" + self.test_submode_id + "/submodel-elements/" + "list_1")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
