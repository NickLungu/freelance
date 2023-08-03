from PIL import Image


class ImageResizer:
    def __init__(self, image_file, x, y):
        self.image_file = image_file
        self.side_x = None if x is None else int(x)
        self.side_y = None if y is None else int(y)
        self.resized_image = None

    def resize_image(self):

        im1 = Image.open(self.image_file)

        width, height = im1.size
        coef_ = 1

        # считаем коэффициент как отношение нового и старого размера
        if not self.side_x is None:
            coef_ = self.side_x / width

        elif not self.side_y is None:
            coef_ = self.side_y / height

        width_new = width * coef_
        height_new = height * coef_
        # resize image
        self.resized_image = im1.resize((int(width_new), int(height_new)))
        return self.resized_image

    def save_to_file(self, file_path):
        # сохраняем файл без кодировки в base64, так как мы не показываем миниатюру
        resized_image = self.resized_image
        resized_image.save(file_path)
