from flask import Response


def test_labels_all(client):
    """ Query all labels """
    all_labels: Response = client.get('/api/labels/all')
    assert all_labels.status_code == 200
    assert len(all_labels.json) == 4
    assert set(label['name'] for label in all_labels.json) == {'l_a', 'l_b', 'l_c', 'l_d'}


def test_labels_label(client):
    """ Test api endpoint for individual label """
    all_labels: Response = client.get('/api/labels/all')

    for label_dict in all_labels.json:
        uri = label_dict['uri']
        label_id = label_dict['label_id']
        assert uri == f'/api/labels/label/{label_id}'
        label_name = label_dict['name']
        label: Response = client.get(uri)
        assert label.json['label_id'] == label_id
        assert label.json['name'] == label_name


def test_labels_label_assignment(client):
    """ Test api endpoint for individual label_assignments """
    images: Response = client.get('/api/query/images/l_a')

    for image in images.json:
        assignments = image['label_assignments']
        assignment = [a for a in assignments if a['label']['name'] == 'l_a'][0]
        assignment_id = assignment['label_assignment_id']
        uri = assignment['uri']
        assert uri == f'/api/labels/assignment/{assignment_id}'
        label_name = assignment['label']['name']
        assert 'l_a' == label_name
