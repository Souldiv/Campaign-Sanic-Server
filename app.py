from sanic import Sanic
from sanic_cors import CORS
import asyncio
import uvloop


asyncio.set_event_loop(uvloop.new_event_loop())
app = Sanic("Heros legacy")
CORS(app, resources={r"/*": {"origins": "*"}})
