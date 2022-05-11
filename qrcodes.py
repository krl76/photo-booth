import qrcode
import uuid


def generate_qr():
    data = 'place for website'
    img = qrcode.make(data)
    path = f'qrcodes/{uuid.uuid1()}.png'
    img.save(path)
    return path
