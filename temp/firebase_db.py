import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
import asyncio

cred = credentials.Certificate('firebase_/the_firebase_key.json')
def_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'lazarus-c11d5.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()


async def upload_blob(fileloc, name, loop):
    if name.split('.')[1] == 'html':
        print(name.split('.')[1])
        theFile = bucket.blob("templates/" + name)
    else:
        print("hasdahsd")
        theFile = bucket.blob("attachments/" + name)
    try:
        theFile.upload_from_filename(fileloc)
        return True
    except Exception as e:
        return False


@asyncio.coroutine
def list_files(loop):
    result = yield from loop.run_in_executor(None, bucket.list_blobs)
    return result
