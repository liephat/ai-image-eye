from flask import Response

def test_labels_all(client):
    all_labels: Response = client.get('/api/labels/all')
    assert all_labels.status_code == 200
    assert len(all_labels.json) > 0
    assert set(l['name'] for l in all_labels.json) == {'a', 'b', 'c', 'd'}
