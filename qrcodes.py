import qrcode
import uuid

UID = uuid.uuid1()


def qr():
    data = 'place for website'
    img = qrcode.make(data)
    path = f'qrcodes/{UID}.png'
    img.save(path)
    return path
