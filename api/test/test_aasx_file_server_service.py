import unittest
from fastapi.testclient import TestClient

from server import app
from .examples.aasx_packages import aasx_package_json
from .examples.submodels import test_submodel_modified, test_submodel

client = TestClient(app)
BASE_URL = "/api/v3.0/"


class TestFastAPIEndpoints(unittest.TestCase):
    test_aasx_package_id = aasx_package_json["id"]
    invalid_submodel_id = "some_blob"

    def test_01_get_all_aasx_package_ids(self):
        # Test the GET / endpoint
        response = client.get(BASE_URL + "aasx/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_02_post_aasx_package(self):
        response = client.post(BASE_URL + "aasx/", json=aasx_package_json)
        self.assertEqual(response.status_code, 200)

    def test_03_get_aasx_package(self):
        response_test_entry = client.get(BASE_URL + "aasx/" + self.test_aasx_package_id + "/")
        self.assertEqual(response_test_entry.status_code, 200)
        self.assertEqual(response_test_entry.json(), aasx_package_json)

    def test_04_delete_aasx_package(self):
        pass

    def test_05_put_aasx_package(self):
        pass


if __name__ == "__main__":
    unittest.main()
