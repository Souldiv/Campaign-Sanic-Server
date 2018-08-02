import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

cred = credentials.Certificate('firebase_/the_firebase_key.json')
def_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'lazarus-c11d5.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()


async def upload_blob(fileloc, name):
    if name.split('.')[1] == 'html':
        theFile = bucket.blob("templates/" + name)
    else:
        theFile = bucket.blob("attachments/" + name)
    theFile.upload_from_filename(fileloc)
    return True
