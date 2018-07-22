from exceptions.exceptions import *
from handlers.handlers import *
from app import app
import asyncio

if __name__ == '__main__':
    server = app.create_server(host="0.0.0.0", port=6969)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)
    loop.run_forever()