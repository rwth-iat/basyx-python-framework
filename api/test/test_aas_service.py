import os
import json
import unittest
from fastapi.testclient import TestClient

from server import app

BASE_URL = "/api/v3.0/"


class TestAASService(unittest.TestCase):
    def setUp(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.client = TestClient(app)

        with open(os.path.join(base_path, "examples", "aas.json"), encoding="utf-8") as f:
            self.aas_example = json.load(f)

        self.shell_example_id = self.aas_example["id"]
        self.invalid_shell_example_id = "some_other_id"

    def test_aas_post(self):
        response = self.client.post(BASE_URL + "aas/shells", json=self.aas_example)
        self.assertEqual(response.status_code, 200)

        # Teardown
        self.client.delete(BASE_URL + "aas/shells/" + self.shell_example_id)

    def test_get_all_shells(self):
        response = self.client.get(BASE_URL + "aas/shells")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # Setup
        self.client.post(BASE_URL + "aas/shells", json=self.aas_example)

        response = self.client.get(BASE_URL + "aas/shells")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.aas_example])

        # Teardown
        self.client.delete(BASE_URL + "ass/shells/" + self.shell_example_id)

    def test_get_specific_shell(self):
        # Setup
        self.client.post(BASE_URL + "aas/shells", json=self.aas_example)

        response_test_undefined = self.client.get(BASE_URL + "aas/shells/" + self.invalid_shell_example_id)
        response_test_entry = self.client.get(BASE_URL + "aas/shells/" + self.shell_example_id)

        self.assertEqual(response_test_undefined.status_code, 404)
        self.assertEqual(response_test_entry.status_code, 200)
        self.assertEqual(response_test_entry.json(), self.aas_example)

        # Teardown
        self.client.delete(BASE_URL + "submodels/" + self.shell_example_id + "/")

    # FIXME: Technically a test_delete_shell would be added here. Is this really necessary?


if __name__ == "__main__":
    unittest.main()
