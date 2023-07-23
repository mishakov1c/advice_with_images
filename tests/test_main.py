from unittest.mock import patch
from fastapi.testclient import TestClient
from webapp import main


def test__get_advice__success():
    with (
        patch('webapp.main.get_bored_activity') as get_bored_activity_mock,
        patch('webapp.main.get_unsplash_picture') as get_unsplash_picture_mock,
    ):

        get_bored_activity_mock.return_value = "Research a topic you're interested in"
        get_unsplash_picture_mock.return_value = "https://images.unsplash.com/photo-153218786.jpg"

        client = TestClient(main.app)
        response = client.get("/")

        assert response.status_code == 200
        assert response.template.name == 'index.html'
        assert response.context['activity'] == "Research a topic you're interested in"
        assert response.context['picture_link'] == "https://images.unsplash.com/photo-153218786.jpg"

        get_bored_activity_mock.assert_called_once()
        get_unsplash_picture_mock.assert_called_once_with("Research a topic you're interested in")
