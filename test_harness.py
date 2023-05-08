from app import create_app
import pytest
from werkzeug.test import Client

class TestHarness:

    
    def test1(self):
        assert 1 == 1

    @pytest.fixture()
    def app(self):
        app = create_app()
        app.config.update({
            "TESTING": True,
        })

        # other setup can go here

        yield app

        # clean up / reset resources here

    @pytest.fixture()
    def client(app):
        return app.test_client()

    @pytest.fixture()
    def runner(app):
        return app.test_cli_runner()
    
    def test_request_example(self):
        client = Client(create_app())
        response = client.get("/")
        assert response.get_data() == b'{"name": "test message", "message": "The API is working"}'