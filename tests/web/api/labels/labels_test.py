from flask import Response


def test_labels_all(client):
    all_labels: Response = client.get('/api/labels/all')
    assert all_labels.status_code == 200
    assert len(all_labels.json) == 4
    assert set(label['name'] for label in all_labels.json) == {'l_a', 'l_b', 'l_c', 'l_d'}
