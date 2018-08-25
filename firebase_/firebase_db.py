import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
import asyncio

cred = credentials.Certificate('firebase_/the_firebase_key.json')
def_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'lazarus-c11d5.appspot.com'
})


loop = asyncio.get_event_loop()
db = firestore.client()
bucket = storage.bucket()


async def upload_blob(fileloc, name):
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
def list_files(settings=True):
    result = yield from loop.run_in_executor(None, bucket.list_blobs)
    to_replace = "https://storage.googleapis.com/lazarus-c11d5.appspot.com/"
    result = [blobx for blobx in result]
    formatted_result = [one.public_url.replace(
        to_replace, "") for one in result]
    if settings:
        return formatted_result
    else:
        return result, formatted_result
