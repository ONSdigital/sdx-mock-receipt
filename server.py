from functools import wraps
import logging
import os
import xml.etree.ElementTree as ET

from flask import Flask, make_response, request, render_template
from structlog import wrap_logger

import settings

app = Flask(__name__)

logging.basicConfig(format=settings.LOGGING_FORMAT,
                    datefmt="%Y-%m-%dT%H:%M:%S",
                    level=settings.LOGGING_LEVEL)

logger = wrap_logger(logging.getLogger(__name__))


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == settings.RECEIPT_USER and password == settings.RECEIPT_PASS


def authenticate():
    """Sends a 401 response that enables basic auth"""
    # TODO: return appropriate auth error xml
    resp = make_response(render_template('error.xml'), 401)
    resp.headers['Content-Type'] = 'application/vnd.ons.error+xml'
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.errorhandler(400)
def not_found(error):
    resp = make_response(render_template('error.xml'), 400)
    resp.headers['Content-Type'] = 'application/vnd.ons.error+xml'
    return resp


@app.route('/receipts', methods=['POST'])
def receipt():
    return make_response('{"status": "ok"}', 200)


@app.route('/reportingunits/<ru_ref>/collectionexercises/<exercise_sid>/receipts', methods=['POST'])
@requires_auth
def ack(ru_ref, exercise_sid):

    if len(ru_ref) != 11 or len(exercise_sid) != 11:
        logger.warning("Got an invalid ru_ref/exercise_sid", ru_ref=ru_ref, exercise_sid=exercise_sid)

    logger.debug("Got a response", ru_ref=ru_ref, exercise_sid=exercise_sid)

    data = request.get_data()
    logger.debug("Received Headers: {0}".format(request.headers))
    logger.debug("Received XML Receipt: {0}".format(data.decode('UTF8')))

    receipt_xml = ET.fromstring(data)
    ns = {'receipt': 'http://ns.ons.gov.uk/namespaces/resources/receipt'}

    respondent = receipt_xml.find('receipt:respondent_id', ns)
    respondent_id = respondent.text

    if respondent_id:
        logger.debug("Confirmed receipt for respondent", respondent_id=respondent_id)
        return respondent_id, 201
    else:
        return not_found("Couldn't parse respondent_id")

if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
