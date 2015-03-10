import os
import responses
import requests

@responses.activate
def test_my_api():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')
    print resp
    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.text == '{"error": "not found"}'

@responses.activate
def test_github_api():
    # os.path.join(os.path.dirname(__file__), 'my_file')
    dir = os.getcwd()
    with open(dir + 'deploy_tix/tests/api.github.com/repos/mozmock-services/hollow-deck/git/tags') as f:
        data = f.read()
        print data


