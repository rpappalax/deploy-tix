import os
import responses
import requests


@responses.activate
def test_my_api():
    responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                  body='{"error": "not found"}', status=404,
                  content_type='application/json')

    resp = requests.get('http://twitter.com/api/1/foobar')
    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://twitter.com/api/1/foobar'
    assert responses.calls[0].response.text == '{"error": "not found"}'


@responses.activate
def test_get_tags():
    domain = 'https://api.github.com'
    dir_local = 'deploy_tix/tests/mocks/api.github.com'
    path = 'repos/mozilla-services/shavar/git/tags'
    path_local = ''
    path_local = path_local +'deploy_tix/tests/mocks/api.github.com/repos/mozilla-services/shavar/git/refs/tags'

    with open(path_local) as f:
        mock_data = f.read()

    path = os.path.join(domain, path)
    responses.add(responses.GET, path,
                  body=mock_data, status=200,
                  content_type='application/json')

    # This is a remote request!!!
    print '*********************************'
    print path
    resp = requests.get(path)
    assert resp.status_code == 200
    # if <Response [200]>,
    print resp
    print resp.json()

    assert len(responses.calls) == 1
    print '================='
    print 'response.callslen: {}'.format(len(responses.calls))
    assert responses.calls[0].request.url == path
    print '================='
    assert responses.calls[0].response.text == mock_data
    print 'responses.calls[0].request.url: {}'.format(responses.calls[0].request.url)
    print 'responses.calls[0].response.text: {}'.format(responses.calls[0].response.text)
    print '================='
    assert(False)

# @responses.activate
# def test_github_api():
#     # dir = os.getcwd()
#     # with open(dir + 'deploy_tix/tests/api.github.com/repos/mozmock-services/'
#     #                 'hollow-deck/git/tags') as f:
#
#     path = os.path.join('deploy_tix/tests/mocks/api.github.com/repos/mozmock-services/hollow-deck/git', 'tags')
#     with open(path) as f:
#         tags_text = f.read()



