from sanic.exceptions import ServerError, NotFound
from sanic import response as res
from app import app
import logging

log = logging.getLogger()


@app.exception(NotFound)
async def ignore_404(request, exception):
    print("INSIDE HERE")
    return res.redirect("http://dscvit.com")


@app.exception(ServerError)
async def handle_exception(request, exception):
    if str(exception.status_code) == '500':
        log.exception('500')
    else:
        log.warning("Bad Request:  "+str(exception)+ " "+ str(exception.status_code))
    return res.redirect("http://google.com")
