from PIL import Image
import io


class ImageConverter:
    def __init__(self, image_file, format):
        self.image_file = image_file
        self.format = format
        self.converted_image = None

    def convert_to_new_format(self):
        image = Image.open(self.image_file)
        converted_image = io.BytesIO()
        if image.mode == 'RGBA' and self.format != 'PNG':
            # конвертируем RGBA в RGB if если новый формат не png
            # иначе файл не сохранится в другом формате из-за альфа-канала
            image = image.convert('RGB')
        image.save(converted_image, format=self.format)
        converted_image.seek(0)
        self.converted_image = converted_image
        return converted_image

    def save_to_file(self, file_path):
        converted_image = self.converted_image
        with open(file_path, 'wb') as file:
            file.write(converted_image.getvalue())

