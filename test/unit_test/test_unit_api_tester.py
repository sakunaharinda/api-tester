import sys
from unittest.mock import patch

sys.path.insert(1, '../app')
import json
from app import api_tester
from h2o_wave import Q, FormCard


def test_delete_header():
    h = {'abs': 'abs'}
    content = api_tester.delete_header(0, h)
    assert content == {}


@patch("h2o_wave.Q")
def test_show_dialog(q: Q):
    api_tester.show_dialog(q)

    dialog = q.page['meta'].dialog
    assert dialog.title == 'Error'
    assert dialog.items[0].text.content == 'Key and Value pair both should be filled!'
    assert dialog.items[1].buttons.items[0].button.label == 'OK'


def test_body():
    body: FormCard = api_tester.body()
    assert body.items[1].textbox.name == 'text'


def test_headers():
    headers: FormCard = api_tester.headers()
    assert headers.items[0].text_l.content == "Request headers"
    assert headers.items[1].inline.items[2].button.name == "addHeader"
    assert headers.items[2].table.columns[0].name == "id"


def get_response():
    with open('resp.json') as f:
        return json.load(f)


def test_send_get():
    fake_json = get_response()

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = fake_json
        mock_get.return_value.status_code = 200

        resp = api_tester.send('url', 'GET')

    assert resp == str(fake_json)


def test_send_post():
    fake_json = get_response()

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = fake_json
        mock_post.return_value.status_code = 200

        resp = api_tester.send('url', 'POST')

    assert resp == str(fake_json)
