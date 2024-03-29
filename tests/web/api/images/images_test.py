from flask import Response


def test_images_all(client):
    all_images: Response = client.get('/api/images/all')
    assert all_images.status_code == 200
    assert len(all_images.json) > 0
    assert any(image['file'] == 'file1.jpg' for image in all_images.json)
    assert any(image['url'] == '/images/?name=file1.jpg' for image in all_images.json)
    assert any(set(l['label']['name'] for l in image['label_assignments']) == {'l_a', 'l_d'}
               and image['file'] == 'file4.jpg'
               for image in all_images.json)
