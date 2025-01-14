import unittest
from fastapi.testclient import TestClient
from server import app  # Import your FastAPI app

# Create a TestClient instance for your app
client = TestClient(app)

class TestFastAPIEndpoints(unittest.TestCase):
    def test_registry_submodel_descriptors(self):
        # Test the GET /items/{item_id} endpoint
        response = client.get("/api/v3.0/submodels/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


if __name__ == "__main__":
    unittest.main()
