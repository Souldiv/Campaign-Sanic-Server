from sanic.response import json
from app import app
import motor.motor_asyncio
from sanic.exceptions import ServerError
import sanic.log
import sanic.response as response

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://Souldiv:ballsdeep78@ds145981.mlab.com:45981/heroku_hv9lg70l')


@app.route("/campaign", methods=['GET'])
async def sample_data(request):
    print("HERE AMRUT ",request.args)
    try:
        redirect_url = request.args['next'][0]
        print("REDIRECT URL ",redirect_url)
        document = {
        'fest_id': request.args['fest'][0],
        'campaign_id': request.args['cid'][0],
        'source': request.args['source'][0]
        }
        print("THIS document ", document)
    except KeyError:
        raise ServerError("Key error, somebody trampled with the url", status_code=400)
    db = client['heroku_hv9lg70l']
    collection = db['campaign']
    collection.insert_one(document)
    return response.redirect(redirect_url)


@app.route("/raise", methods=['GET'])
async def rasi(request):
    raise ServerError("Something good happened", status_code=400)
    return json({
        "lets see": "if it returns"
    })


@app.route("/db", methods=['GET'])
async def test_db(request):
    db = client['heroku_hv9lg70l']
    collection = db['campaign']
    document = {'campaign_name': 'hello world!'}
    result = await collection.insert_one(document)
    return json({
        'inserted_id': 'something'
    })


@app.route("/redirect", methods=['GET'])
async def fornicate(req):
    return response.redirect('web.telegram.org')
