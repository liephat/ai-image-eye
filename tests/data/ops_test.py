from app.data.ops import ImageDataHandler


def test_filtered_images(client):
    ImageDataHandler.add_label_assignment('file4.jpg', 'l_ax', 'user')
    ImageDataHandler.add_label_assignment('file2.jpg', 'xl_cx', 'user')

    images = ImageDataHandler.filtered_images('l_a')
    assert sorted(image.file for image in images) == ['file has spaces.jpg', 'file1.jpg',
                                                      'file2.jpg', 'file4.jpg']

    images = ImageDataHandler.filtered_images('l*a')
    assert sorted(image.file for image in images) == ['file has spaces.jpg', 'file1.jpg',
                                                      'file2.jpg', 'file4.jpg']

    images = ImageDataHandler.filtered_images('*c*')
    assert sorted(image.file for image in images) == ['file2.jpg', 'file3.jpg']

    images = ImageDataHandler.filtered_images('*')
    assert sorted(image.file for image in images) == ['file has spaces.jpg', 'file1.jpg',
                                                      'file2.jpg', 'file3.jpg', 'file4.jpg']

def test_bounding_box(client):
    ImageDataHandler.add_label_assignment('file1.jpg', 'label_with_bb', 'bb_tester', 0.9,
                                          dict(l=0.2, r=0.3, t=0.1, b=0.5))

    assignments = ImageDataHandler.get_assignments_from_origin('file1.jpg', 'bb_tester')
    assert assignments[0].box == {'bottom': 50.0, 'left': 20.0, 'right': 70.0, 'top': 10.0}
    assert assignments[0].confidence == 0.9

    # no box
    assignments = ImageDataHandler.get_assignments_from_origin('file1.jpg', 'nnet')
    assert assignments[0].box is None

