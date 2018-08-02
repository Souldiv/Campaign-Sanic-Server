from sanic.exceptions import ServerError, NotFound, SanicException
from sanic import response as res
from app import app
import logging
import datetime

log = logging.getLogger()


@app.exception(NotFound)
async def ignore_404(request, exception):
    now = datetime.datetime.now(datetime.timezone.utc)
    strfz = now.strftime("%Y-%m-%d %H:%M:%S")
    log.error("[" + strfz + " GMT ] " + str(exception) +
              " [" + str(exception.status_code) + "]")

    return res.redirect("http://dscvit.com")


@app.exception(ServerError)
async def handle_server_exception(request, exception):
    print("Inside server error")
    now = datetime.datetime.now(datetime.timezone.utc)
    strfz = now.strftime("%Y-%m-%d %H:%M:%S")
    log.error("[" + strfz + " GMT ] " + str(exception) +
              " [" + str(exception.status_code) + "]")
    return res.redirect("http://dscvit.com")


@app.exception(SanicException)
async def custom_exception(request, exception):
    print("Inside Sanic exception ")
    if exception.status_code == 215:
        res.status_code = 400
        return res.json({
            "error": "Unauthorized",
            "status_code": 215
        }, status=400)

    elif exception.status_code == 216:
        return res.json({
            'error': str(exception),
            'status_code': 400
        }, status=400)

    elif exception.status_code == 217:
        now = datetime.datetime.now(datetime.timezone.utc)
        strfz = now.strftime("%Y-%m-%d %H:%M:%S")
        log.error("[" + strfz + " GMT ] " + str(exception) +
                  " [" + str(exception.status_code) + "]")
        return res.json({
            'message': 'Unauthorized',
            'status_code': 400
        }, status=400)

    now = datetime.datetime.now(datetime.timezone.utc)
    strfz = now.strftime("%Y-%m-%d %H:%M:%S")
    log.error("[" + strfz + " GMT ] " + str(exception) +
              " [" + str(exception.status_code) + "]")
    return res.redirect("http://dscvit.com")
