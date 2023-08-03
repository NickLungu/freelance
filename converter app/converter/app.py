import base64
import logging
import os
import time

from flask import Flask, request, render_template, session, send_file
from classes.converter import ImageConverter
from classes.resizer import ImageResizer

app = Flask(__name__)
app.secret_key = "11111"

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route('/')
@app.route('/about_us')
def main():
    request_path = '/about_us'
    return render_template('about_us.html',request_path=request_path)


@app.route('/convert')
def convert_page():
    request_path = '/convert'
    return render_template('convert.html',request_path=request_path)


@app.route('/resize')
def resize_page():
    request_path = '/resize'
    return render_template('resize.html',request_path=request_path)


@app.route('/convert', methods=['POST'])
def convert():
    request_path = '/convert'
    try:
        image = request.files['image']
        format = request.form['format']
    except Exception as e:
        logging.error(f'Just a page or error retrieving image or format: {e}')
        return render_template('convert.html',request_path=request_path)

    converter = ImageConverter(image, format)
    converted_image = converter.convert_to_new_format()
    media_dir = os.path.join(app.root_path, 'media')
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)

    # создаем путь для файла с уникальным идентификатором
    path = os.path.join(media_dir, "image_%s.%s" % ((str(int(time.time() * 1000))), format))
    converter.save_to_file(path)

    session['path'] = path
    session['format'] = format
    logging.info(path)
    logging.info('Image conversion successful')
    converted_image_base64 = base64.b64encode(converted_image.getvalue()).decode('utf-8')
    return render_template('convert.html', converted_image=converted_image_base64, request_path=request_path)


@app.route('/resize', methods=['POST'])
def resize():
    request_path = '/resize'
    try:
        image = request.files['image']
        side = request.form['side']
        px_value = int(request.form.get('px'))
        logging.info(side)
        logging.info(px_value)
        if px_value < 50 or px_value > 1000:
            raise Exception("size in px is not valid")
    except Exception as e:
        logging.error(f'Just a page or error retrieving image or format: {e}')
        return render_template('resize.html', request_path=request_path)

    image_extension = os.path.splitext(image.filename)[1][1:].lower()

    if side == 'x':
        resizer = ImageResizer(image, px_value, None)
    else:
        resizer = ImageResizer(image, None, px_value)
    resized_image = resizer.resize_image()

    media_dir = os.path.join(app.root_path, 'media')
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)

    path = os.path.join(media_dir, "image_%s.%s" % (str(int(time.time() * 1000)), image_extension))
    resizer.save_to_file(path)

    # сохраняем в сессии данные
    session['path'] = path
    session['format'] = image_extension
    logging.info(path)
    logging.info('Image resizing successful')
    resized_image_base64 = base64.b64encode(resized_image.tobytes()).decode('utf-8')
    return render_template('resize.html', resized_image=resized_image_base64, request_path=request_path)


@app.route('/download')
def download():
    logging.info(session)
    if 'path' in session:
        image_path = session['path']
        format = session['format']
        # Set the appropriate MIME type based on the format
        mime_types = {
            'jpeg': 'image/jpeg',
            'jpg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif'
        }
        # указываем формат документа, который отправляем для скачивания
        # благодаря application/octet-stream браузер предложит скачать файл
        mime_type = mime_types.get(format, 'application/octet-stream')

        file_name_session = session['path'].split('\\')[-1]
        media_dir = os.path.join(app.root_path, 'media')
        # удаляем все файлы кроме файла сессии
        # чтобы не копился мусор
        for file_name in os.listdir(media_dir):
            file_path = os.path.join(media_dir, file_name)
            if os.path.isfile(file_path) and file_name != file_name_session:
                os.remove(file_path)

        return send_file(image_path, mimetype=mime_type, as_attachment=True)
    else:
        return 'No processed image found.'


if __name__ == '__main__':
    logging.info('app start')
    app.run()
