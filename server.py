import logging
import os

from flask import Flask, make_response, request
from structlog import wrap_logger

import settings

app = Flask(__name__)

logging.basicConfig(format=settings.LOGGING_FORMAT,
                    datefmt="%Y-%m-%dT%H:%M:%S",
                    level=settings.LOGGING_LEVEL)

logger = wrap_logger(logging.getLogger(__name__))


@app.route('/receipts', methods=['POST'])
def receipt():
    if request.mimetype != 'application/json':
        logger.error("Content type 'application/json' not set")
        return make_response('{"status": "error"}', 400)

    receipt_json = request.get_json()

    if not receipt_json.get('caseId'):
        logger.error("Missing caseId from receipt json")
        return make_response('{"status": "error"}', 400)

    logger.info("Successfully recieved receipt", case_id=receipt_json['caseId'])
    return make_response('{"status": "ok"}', 201)


if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
