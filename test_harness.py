import requests

class TestHarness:

    def test1(self):
        assert 1 == 1
        
    def test_index_page(self):
        url = 'http://127.0.0.1:8080'
        r = requests.get(url+'/') # Assumses that it has a path of "/"
        assert r.status_code == 200 # Assumes that it will return a 200 response
