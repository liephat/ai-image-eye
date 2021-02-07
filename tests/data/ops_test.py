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
