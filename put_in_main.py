from db_data import db_session
from db_data.photos import Photo
from random import choices


db = db_session.create_session()
photo = Photo()
photo.photo = 'img'
generate_code = choices(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], k=8)
photo.code = generate_code
db.add(photo)
db.commit()
       
def main():
    db_session.global_init('db/photo-booth.sqlite')
    app.run()

